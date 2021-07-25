from typing import List, Protocol

from ...graphql import GraphQLContext
from ...hooks import FilterHook
from ..types import ParsedMarkupMetadata


class UpdateMarkupMetadataAction(Protocol):
    async def __call__(
        self, context: GraphQLContext, ast: List[dict], metadata: ParsedMarkupMetadata
    ):
        ...


class UpdateMarkupMetadataFilter(Protocol):
    async def __call__(
        self,
        action: UpdateMarkupMetadataAction,
        context: GraphQLContext,
        ast: List[dict],
        metadata: ParsedMarkupMetadata,
    ):
        ...


class UpdateMarkupMetadataHook(
    FilterHook[UpdateMarkupMetadataAction, UpdateMarkupMetadataFilter]
):
    def call_action(
        self,
        action: UpdateMarkupMetadataAction,
        context: GraphQLContext,
        ast: List[dict],
        metadata: ParsedMarkupMetadata,
    ):
        return self.filter(action, context, ast, metadata)


update_markup_metadata_hook = UpdateMarkupMetadataHook()