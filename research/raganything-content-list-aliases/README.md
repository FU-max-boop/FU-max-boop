# RAG-Anything Content-List Alias Handling

Upstream PR: https://github.com/HKUDS/RAG-Anything/pull/273

This contribution tightens RAG-Anything's direct `content_list` multimodal
processing path so already-parsed multimodal items keep useful alias fields
instead of silently dropping or misformatting them.

## Finding

The direct `content_list` path can receive table, equation, image, and caption
fields from slightly different upstream parsers. In that path:

- a table with only `table_data` can produce an empty table body
- an equation with only `latex` can lose its formula text
- string captions can be joined character-by-character
- text/multimodal separation can lose the item's original `content_list` index

## Fix

The PR:

- preserves each multimodal item's original `content_list` index
- normalizes string/list captions and footnotes
- reads table content from `table_body`, `table_data`, or `text`
- reads equation content from `text`, `latex`, or `equation`
- infers `LaTeX` format when only `latex` is provided

## Validation

From the upstream repo root:

```bash
python3 -m py_compile raganything/utils.py raganything/processor.py raganything/modalprocessors.py tests/test_content_list_alias_handling.py
python3 -m unittest tests/test_content_list_alias_handling.py
git diff --check
```

Scope: this does not change parsers, model calls, retrieval behavior, or prompt
templates. It only normalizes already-parsed multimodal fields before building
chunks and prompts.
