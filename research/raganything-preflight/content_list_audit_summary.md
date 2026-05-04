# RAG-Anything Content List Audit

- Generated at: `2026-05-04T15:23:55.566916+00:00`
- Input: `/Users/fu/Desktop/ai study/builds/hku-ai-papers/RAG-Anything/examples/sample_content_list.json`
- Status: `blocked`
- Context mode: `page`
- Context window: `1`
- Context types: `text`
- Total items: 7
- Blockers: 2
- Warnings: 2
- Multimodal items without context: 1

## Type Distribution

| Type | Count |
| --- | ---: |
| `equation` | 1 |
| `image` | 1 |
| `table` | 2 |
| `text` | 3 |

## Findings

| Severity | Item | Type | Field | Finding | Recommendation |
| --- | ---: | --- | --- | --- | --- |
| `fail` | 1 | `image` | `img_path` | Image path looks like a placeholder. | Replace the placeholder with a real absolute image path. |
| `fail` | 1 | `image` | `img_path` | Image path does not exist locally. | Create the file, fix the path, or remove the image item. |
| `warn` | 2 | `table` | `context` | No page-window context was found for this multimodal item. | Add nearby text/captions or increase the context window before insertion. |
| `warn` | 3 | `equation` | `text_format` | Equation has latex but no text_format. | Set text_format to LaTeX so downstream prompts can preserve notation. |

## Item Audit

| Index | Type | Page | Status | Text Chars | Captions | Context Items | Context Chars |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: |
| 0 | `text` | 0 | `pass` | 169 | 0 | 0 | 0 |
| 1 | `image` | 1 | `fail` | 0 | 1 | 1 | 169 |
| 2 | `table` | 2 | `warn` | 283 | 1 | 0 | 0 |
| 3 | `equation` | 3 | `warn` | 136 | 0 | 1 | 196 |
| 4 | `text` | 4 | `pass` | 196 | 0 | 0 | 0 |
| 5 | `table` | 5 | `pass` | 272 | 1 | 2 | 367 |
| 6 | `text` | 6 | `pass` | 171 | 0 | 0 | 0 |
