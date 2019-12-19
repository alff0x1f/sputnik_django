from typing import Dict, List, Tuple

from ariadne import MutationType
from graphql import GraphQLResolveInfo
from pydantic import PositiveInt, constr, create_model

from ...auth import get_authenticated_user
from ...errors import ErrorsList, NotAuthorizedError
from ...hooks import (
    post_thread_hook,
    post_thread_input_hook,
    post_thread_input_model_hook,
)
from ...loaders import store_post, store_thread
from ...threads.create import create_post, create_thread
from ...threads.update import update_thread
from ...types import (
    AsyncValidator,
    GraphQLContext,
    Post,
    PostThreadInput,
    PostThreadInputModel,
    Thread,
)
from ...validation import validate_category_exists, validate_data, validate_model
from ..errorhandler import error_handler


post_thread_mutation = MutationType()


@post_thread_mutation.field("postThread")
@error_handler
async def resolve_post_thread(
    _, info: GraphQLResolveInfo, *, input: dict  # pylint: disable=redefined-builtin
):
    user = await get_authenticated_user(info.context)
    if not user:
        raise NotAuthorizedError()

    input_model = await post_thread_input_model_hook.call_action(
        create_input_model, info.context
    )
    cleaned_data, errors = validate_model(input_model, input)

    if cleaned_data:
        validators = {
            "category": [validate_category_exists(info.context)],
        }
        cleaned_data, errors = await post_thread_input_hook.call_action(
            validate_input_data, info.context, validators, cleaned_data, errors
        )

    if errors:
        return {"errors": errors}

    thread, _ = await post_thread_hook.call_action(
        post_thread, info.context, cleaned_data
    )

    return {"thread": thread}


async def create_input_model(context: GraphQLContext) -> PostThreadInputModel:
    return create_model(
        "PostThreadInputModel",
        category=(PositiveInt, ...),
        title=(constr(strip_whitespace=True), ...),
        body=(constr(strip_whitespace=True), ...),
    )


async def validate_input_data(
    context: GraphQLContext,
    validators: Dict[str, List[AsyncValidator]],
    cleaned_data: PostThreadInput,
    errors: ErrorsList,
) -> Tuple[PostThreadInput, ErrorsList]:
    return await validate_data(cleaned_data, validators, errors)


async def post_thread(
    context: GraphQLContext, cleaned_data: PostThreadInput
) -> Tuple[Thread, Post]:
    user = await get_authenticated_user(context)
    thread = await create_thread(
        cleaned_data["category"], cleaned_data["title"], starter=user
    )
    post = await create_post(thread, {"text": cleaned_data["body"]}, poster=user)
    thread = await update_thread(thread, first_post=post, last_post=post)

    store_thread(context, thread)
    store_post(context, post)

    return thread, post