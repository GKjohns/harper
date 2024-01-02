from ..bronco import (GPT_3_5_TURBO, GPT_4, GEMINI_PRO, VALID_MODELS, llm_call, LLMFunction)

summarizer_prompt = '''
# Task
Please summarize the text below.
Ensure that your summary is at most {output_word_count} words.
Be sure to include the most important information.
Do not include any commentary other than your summary.
If it seems like there are jumps or its incoherent, do your best to make the summary coherent.


# Text to summarize
{text}


# Your output (only a summary that is at most {output_word_count} words)
'''


def summarize(doc, output_word_count):
    
    summarizer = LLMFunction(summarizer_prompt)
    summary = summarizer.generate({
        'text': doc,
        'model': GPT_3_5_TURBO,
        'output_word_count': output_word_count
    })
    return summary

def chunk_document(doc, chunk_size):
        words = doc.split(' ')
        total_words = len(words)
        chunk_count = -(-total_words // chunk_size)  # Calculate number of chunks using ceiling division

        for i in range(chunk_count):
            start_index = i * chunk_size
            end_index = min(start_index + chunk_size, total_words)
            yield ' '.join(words[start_index:end_index])


    

def recursive_summarize(document, max_chunk_size=1000, output_word_count=200):
    """
    Summarizes a large document by breaking it into smaller chunks, summarizing each, and then
    recursively summarizing the combined summaries until the final summary is within the desired word count.

    :param document: The large document to summarize.
    :param max_chunk_size: The maximum word count for each chunk (4,000 in this case).
    :param output_word_count: The desired word count for the final summary.
    :return: The final summarized document.
    """
    
    # we have a digestible chunk size
    if len(document.split(' ')) <= max_chunk_size:
        return summarize(document, output_word_count)

    # Break out into chunks and summarize the chunks
    chunks = list(chunk_document(document, max_chunk_size))
    summarized_chunk_max_size = max_chunk_size // len(chunks)
    summarized_chunks = [summarize(chunk, summarized_chunk_max_size) for chunk in chunks]

    # Combine the chunks 
    combined_summaries = summarize(
        document='\n\n'.join(summarized_chunks),
        max_chunk_size=max_chunk_size,
    )

    # We need to split again
    if len(combined_summary.split(' ')) > max_chunk_size:
        return recursive_summarize(combined_summaries, max_chunk_size, output_word_count)

    # The summary is digestible
    return summarize(combined_summary, output_word_count)