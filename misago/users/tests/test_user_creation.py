from datetime import datetime

import pytest

from ...passwords import verify_password
from ..create import create_user
from ..get import get_user_by_id


@pytest.mark.asyncio
async def test_user_is_created_in_db(db):
    user = await create_user("test", "test@example.com")
    assert user.id
    assert user == await get_user_by_id(user.id)


@pytest.mark.asyncio
async def test_user_is_created_with_slug(db):
    user = await create_user("TeST", "test@example.com")
    assert user.slug == "test"


@pytest.mark.asyncio
async def test_user_is_created_with_default_join_datetime(db, user_password):
    user = await create_user("test", "test@example.com")
    assert user.joined_at


@pytest.mark.asyncio
async def test_user_is_created_with_specifed_join_datetime(db, user_password):
    joined_at = datetime.utcnow()
    user = await create_user("test", "test@example.com", joined_at=joined_at)
    assert user.joined_at == joined_at


@pytest.mark.asyncio
async def test_user_is_created_with_useable_password(db, user_password):
    user = await create_user("test", "test@example.com", password=user_password)
    assert user.id
    assert await verify_password(user_password, user.password)


@pytest.mark.asyncio
async def test_user_statuses_default_to_false(db, user_password):
    user = await create_user("test", "test@example.com")
    assert not user.is_deactivated
    assert not user.is_moderator
    assert not user.is_admin


@pytest.mark.asyncio
async def test_user_is_created_with_deactivated_status(db, user_password):
    user = await create_user("test", "test@example.com", is_deactivated=True)
    assert user.is_deactivated


@pytest.mark.asyncio
async def test_user_is_created_with_moderator_status(db, user_password):
    user = await create_user("test", "test@example.com", is_moderator=True)
    assert user.is_moderator


@pytest.mark.asyncio
async def test_user_is_created_with_admin_status(db, user_password):
    user = await create_user("test", "test@example.com", is_admin=True)
    assert user.is_admin