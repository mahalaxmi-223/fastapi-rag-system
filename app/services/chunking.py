import re

from models.chunk import Chunk


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = 500,
        overlap_sentences: int = 1
    ):
        self.chunk_size = chunk_size
        self.overlap_sentences = overlap_sentences


    def split_into_paragraphs(
        self,
        text: str
    ) -> list[str]:

        paragraphs = text.split("\n\n")

        return [
            p.strip()
            for p in paragraphs
            if p.strip()
        ]


    def split_into_sentences(
        self,
        paragraph: str
    ) -> list[str]:

        sentences = re.split(
            r'(?<=[.!?])\s+',
            paragraph
        )

        return [
            s.strip()
            for s in sentences
            if s.strip()
        ]


    def create_chunks(
        self,
        text: str
    ) -> list[Chunk]:

        paragraphs = self.split_into_paragraphs(text)


        sentences = []

        for paragraph in paragraphs:
            sentences.extend(
                self.split_into_sentences(paragraph)
            )


        chunks = []

        current_chunk = []
        current_length = 0

        chunk_id = 1
        start_index = 0


        for sentence in sentences:

            sentence_length = len(sentence)

            # What the chunk's length would be if we added this sentence.
            new_length = current_length + sentence_length


            if (
                new_length
                <= self.chunk_size
            ):
                current_chunk.append(sentence)

                current_length = new_length


            else:

                chunk_text = " ".join(current_chunk)


                # NOTE: start_index/end_index are approximate.
                # They accumulate chunk_text lengths, so they don't
                # account for the separators (" ") dropped between
                # chunks or for the overlap sentences carried into
                # the next chunk. Treat them as rough offsets only.
                chunks.append(
                    Chunk(
                        id=chunk_id,
                        text=chunk_text,
                        start_index=start_index,
                        end_index=start_index + len(chunk_text),
                        length=len(chunk_text)
                    )
                )


                chunk_id += 1


                # sentence overlap
                overlap = current_chunk[
                    -self.overlap_sentences:
                ]


                current_chunk = (
                    overlap +
                    [sentence]
                )


                current_length = sum(
                    len(s)
                    for s in current_chunk
                )


                start_index += len(chunk_text)


        # Add remaining text
        # Guard against appending an empty chunk if the last
        # sentence was already flushed on the previous iteration.

        if current_chunk:

            chunk_text = " ".join(current_chunk)

            chunks.append(
                Chunk(
                    id=chunk_id,
                    text=chunk_text,
                    start_index=start_index,
                    end_index=start_index + len(chunk_text),
                    length=len(chunk_text)
                )
            )


        return chunks