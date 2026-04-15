"""Unit tests for rag/embeddings.py — OpenAI calls are fully mocked."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.rag.embeddings import embed_text, embed_texts


def _mock_openai_response(n: int) -> MagicMock:
    """Build a fake openai embeddings response for n inputs."""
    response = MagicMock()
    response.data = [MagicMock(embedding=[0.1 * i] * 1536) for i in range(1, n + 1)]
    return response


@pytest.mark.asyncio
class TestEmbedTexts:
    async def test_returns_one_vector_per_input(self):
        texts = ["clause one", "clause two", "clause three"]
        mock_resp = _mock_openai_response(3)

        with patch("app.rag.embeddings._get_client") as mock_get:
            mock_client = AsyncMock()
            mock_client.embeddings.create = AsyncMock(return_value=mock_resp)
            mock_get.return_value = mock_client

            result = await embed_texts(texts)

        assert len(result) == 3
        assert all(len(v) == 1536 for v in result)

    async def test_empty_input_returns_empty_list(self):
        # Should short-circuit without calling the API
        with patch("app.rag.embeddings._get_client") as mock_get:
            result = await embed_texts([])
            mock_get.assert_not_called()

        assert result == []

    async def test_uses_configured_model(self):
        mock_resp = _mock_openai_response(1)

        with patch("app.rag.embeddings._get_client") as mock_get:
            mock_client = AsyncMock()
            mock_client.embeddings.create = AsyncMock(return_value=mock_resp)
            mock_get.return_value = mock_client

            await embed_texts(["test"])

            call_kwargs = mock_client.embeddings.create.call_args.kwargs
            assert call_kwargs["model"] == "text-embedding-3-small"
            assert call_kwargs["input"] == ["test"]

    async def test_preserves_order(self):
        """Vectors must come back in the same order as inputs."""
        texts = ["first", "second"]
        mock_resp = MagicMock()
        mock_resp.data = [
            MagicMock(embedding=[1.0] * 1536),
            MagicMock(embedding=[2.0] * 1536),
        ]

        with patch("app.rag.embeddings._get_client") as mock_get:
            mock_client = AsyncMock()
            mock_client.embeddings.create = AsyncMock(return_value=mock_resp)
            mock_get.return_value = mock_client

            result = await embed_texts(texts)

        assert result[0][0] == 1.0
        assert result[1][0] == 2.0


@pytest.mark.asyncio
class TestEmbedText:
    async def test_returns_single_vector(self):
        mock_resp = _mock_openai_response(1)

        with patch("app.rag.embeddings._get_client") as mock_get:
            mock_client = AsyncMock()
            mock_client.embeddings.create = AsyncMock(return_value=mock_resp)
            mock_get.return_value = mock_client

            result = await embed_text("single clause")

        assert isinstance(result, list)
        assert len(result) == 1536

    async def test_calls_embed_texts_internally(self):
        """embed_text must delegate to embed_texts (not duplicate logic)."""
        with patch("app.rag.embeddings.embed_texts", new_callable=AsyncMock) as mock_batch:
            mock_batch.return_value = [[0.5] * 1536]
            result = await embed_text("hello")

        mock_batch.assert_awaited_once_with(["hello"])
        assert result == [0.5] * 1536
