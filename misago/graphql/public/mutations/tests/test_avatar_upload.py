import os
from unittest.mock import ANY

import pytest

from .....errors import ErrorsList
from .....testing import override_dynamic_settings
from .....uploads.store import make_media_path
from .....uploads.urls import make_media_url

UPLOAD_AVATAR_MUTATION = """
    mutation AvatarUpload($upload: Upload!) {
        avatarUpload(upload: $upload) {
            user {
                id
                avatars {
                    size
                    url
                }
            }
            errors {
                location
                type
                message
            }
        }
    }
"""


@pytest.mark.asyncio
async def test_upload_avatar_mutation_uploads_avatar(
    query_public_api,
    user,
    test_files_path,
    tmp_media_dir,
):
    result = await query_public_api(
        UPLOAD_AVATAR_MUTATION,
        {
            "upload": (
                "avatar.png",
                open(os.path.join(test_files_path, "avatar.png"), "rb"),
                "image/png",
            ),
        },
        auth=user,
    )

    user_from_db = await user.refresh_from_db()
    assert user_from_db.avatars

    assert result["data"]["avatarUpload"] == {
        "user": {
            "id": str(user.id),
            "avatars": [
                {"size": avatar["size"], "url": make_media_url(avatar["image"])}
                for avatar in user_from_db.avatars
            ],
        },
        "errors": None,
    }

    for avatar in user_from_db.avatars:
        avatar_path = make_media_path(avatar["image"])
        assert os.path.isfile(avatar_path)


@pytest.mark.asyncio
async def test_upload_avatar_mutation_fails_if_user_is_not_authorized(
    query_public_api, user, test_files_path
):
    result = await query_public_api(
        UPLOAD_AVATAR_MUTATION,
        {
            "upload": (
                "avatar.png",
                open(os.path.join(test_files_path, "avatar.png"), "rb"),
                "image/png",
            ),
        },
    )

    assert result["data"]["avatarUpload"] == {
        "user": None,
        "errors": [
            {
                "location": [ErrorsList.ROOT_LOCATION],
                "type": "auth_error.not_authorized",
                "message": "authorization is required",
            },
        ],
    }

    user_from_db = await user.refresh_from_db()
    assert user_from_db.avatars == []


@pytest.mark.asyncio
async def test_upload_avatar_mutation_fails_if_image_has_unsupported_content_type(
    query_public_api, user, test_files_path
):
    result = await query_public_api(
        UPLOAD_AVATAR_MUTATION,
        {
            "upload": (
                "avatar.png",
                open(os.path.join(test_files_path, "avatar.png"), "rb"),
                "image/vnd.adobe.photoshop",
            ),
        },
        auth=user,
    )

    assert result["data"]["avatarUpload"] == {
        "user": {
            "id": str(user.id),
            "avatars": ANY,
        },
        "errors": [
            {
                "location": ["upload"],
                "type": "value_error.upload.content_type",
                "message": (
                    "ensure uploaded file is one of type: "
                    "image/gif, image/jpeg, image/png, image/webp"
                ),
            },
        ],
    }

    user_from_db = await user.refresh_from_db()
    assert user_from_db.avatars == []


@pytest.mark.asyncio
@override_dynamic_settings(avatar_max_size=10)
async def test_upload_avatar_mutation_fails_if_image_file_is_too_large(
    query_public_api, user, test_files_path
):
    result = await query_public_api(
        UPLOAD_AVATAR_MUTATION,
        {
            "upload": (
                "avatar.png",
                open(os.path.join(test_files_path, "avatar.png"), "rb"),
                "image/png",
            ),
        },
        auth=user,
    )

    assert result["data"]["avatarUpload"] == {
        "user": {
            "id": str(user.id),
            "avatars": ANY,
        },
        "errors": [
            {
                "location": ["upload"],
                "type": "value_error.upload.max_size",
                "message": "ensure uploaded file size is not larger than 10 bytes",
            },
        ],
    }

    user_from_db = await user.refresh_from_db()
    assert user_from_db.avatars == []


@pytest.mark.asyncio
async def test_upload_avatar_mutation_fails_if_image_has_unsupported_file_type(
    query_public_api, user, test_files_path
):
    result = await query_public_api(
        UPLOAD_AVATAR_MUTATION,
        {
            "upload": (
                "text_file.txt",
                open(os.path.join(test_files_path, "text_file.txt"), "rb"),
                "image/png",
            ),
        },
        auth=user,
    )

    assert result["data"]["avatarUpload"] == {
        "user": {
            "id": str(user.id),
            "avatars": ANY,
        },
        "errors": [
            {
                "location": ["upload"],
                "type": "value_error.upload.image",
                "message": "ensure uploaded file is valid image",
            },
        ],
    }

    user_from_db = await user.refresh_from_db()
    assert user_from_db.avatars == []


@pytest.mark.asyncio
async def test_upload_avatar_mutation_fails_if_image_is_too_small(
    query_public_api, user, test_files_path
):
    result = await query_public_api(
        UPLOAD_AVATAR_MUTATION,
        {
            "upload": (
                "image.png",
                open(os.path.join(test_files_path, "image.png"), "rb"),
                "image/png",
            ),
        },
        auth=user,
    )

    assert result["data"]["avatarUpload"] == {
        "user": {
            "id": str(user.id),
            "avatars": ANY,
        },
        "errors": [
            {
                "location": ["upload"],
                "type": "value_error.upload.image.min_size",
                "message": "ensure uploaded image size is at least 400x400 pixels",
            },
        ],
    }

    user_from_db = await user.refresh_from_db()
    assert user_from_db.avatars == []