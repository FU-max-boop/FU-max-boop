# Claw-Eval Static Preflight Summary

This report is a local static preflight pass over the public Claw-Eval GitHub repository. It does not run agents, graders, mock services, or model APIs. It checks task metadata and local file references so reproduction work can be scoped before expensive benchmark execution.

## Headline

- Tasks scanned: 300
- Preflight-ready by local metadata/file-reference checks: 232/300
- Blocked by local static issues: 68/300
- Tasks with caution warnings: 105/300

## Split Counts

| Split | Count |
|---|---:|
| general | 161 |
| multi_turn | 38 |
| multimodal | 101 |

## Language Counts

| Language | Count |
|---|---:|
| en | 179 |
| zh | 121 |

## Difficulty Counts

| Difficulty | Count |
|---|---:|
| easy | 74 |
| expert | 1 |
| hard | 104 |
| medium | 118 |
| simple | 3 |

## Top Categories

| Category | Count |
|---|---:|
| workflow | 47 |
| ops | 31 |
| video_qa | 28 |
| what | 26 |
| video_search | 20 |
| doc_extraction | 18 |
| multimodal_webpage | 14 |
| finance | 14 |
| user_agent | 12 |
| office_qa | 10 |
| multimodal | 9 |
| communication | 8 |
| productivity | 7 |
| operations | 6 |
| video_edit | 5 |
| safety | 5 |
| terminal | 5 |
| video_ocr | 3 |
| research | 3 |
| video_webpage | 2 |

## Blocking Issues

| Task | Split | Issue |
|---|---|---|
| M015_video_subtitle_ocr_english | multimodal | missing sandbox files: fixtures/video.webm |
| M016_video_subtitle_ocr_chinese_filter | multimodal | missing sandbox files: fixtures/video.webm |
| M017_video_subtitle_ocr_timestamp | multimodal | missing sandbox files: fixtures/video.webm |
| M022_video_movie_recognition | multimodal | missing sandbox files: fixtures/video.mp4 |
| M023_video_paper_understanding | multimodal | missing sandbox files: fixtures/video.mp4 |
| M024_video_factory_promo_webpage | multimodal | missing sandbox files: fixtures/video.mp4 |
| M025_video_badminton_match_qa | multimodal | missing sandbox files: fixtures/video.mp4 |
| M026_video_story_interactive_webpage | multimodal | missing sandbox files: fixtures/video.mp4 |
| M027_video_food_memo | multimodal | missing sandbox files: fixtures/video.mp4 |
| M028_video_badminton_score_chart | multimodal | missing sandbox files: fixtures/video.mp4 |
| M029_video_surveillance_clip | multimodal | missing sandbox files: fixtures/video.mp4 |
| M030_video_snack_checklist | multimodal | missing sandbox files: fixtures/video.mp4 |
| M031_video_room_floorplan | multimodal | missing sandbox files: fixtures/video.mp4 |
| M032_video_tennis_rally_qa | multimodal | missing sandbox files: fixtures/video.webm |
| M033_video_tennis_breakpoint_qa | multimodal | missing sandbox files: fixtures/video.webm |
| M034_video_tennis_shotlog_qa | multimodal | missing sandbox files: fixtures/video.webm |
| M035_video_tennis_exhibition_qa | multimodal | missing sandbox files: fixtures/video.webm |
| M036_video_butterfly_drawing_tutorial | multimodal | missing sandbox files: fixtures/Dm3nyBNhkp8.mp4 |
| M037_video_food_shop_search | multimodal | missing sandbox files: fixtures/BV1brPYzMEax.mp4 |
| M038_video_lvb_hill_descent | multimodal | missing sandbox files: fixtures/video.mp4 |
| M039_video_lvb_machine_dog | multimodal | missing sandbox files: fixtures/video.mp4 |
| M040_video_lvb_vehicle_identification | multimodal | missing sandbox files: fixtures/video.mp4 |
| M041_video_lvb_artwork_scene | multimodal | missing sandbox files: fixtures/video.mp4 |
| M042_video_mme_multihop_reasoning | multimodal | missing sandbox files: fixtures/video.mp4 |
| M043_video_mme_device_identification | multimodal | missing sandbox files: fixtures/video.mp4 |
| M044_video_mme_bugatti_identification | multimodal | missing sandbox files: fixtures/video.mp4 |
| M045_video_mme_building_identification | multimodal | missing sandbox files: fixtures/video.mp4 |
| M046_video_mme_news_segments | multimodal | missing sandbox files: fixtures/video.mp4 |
| M047_video_fitness_exercise_summary | multimodal | missing sandbox files: fixtures/video.mp4 |
| M048_video_fitness_pullup_frames | multimodal | missing sandbox files: fixtures/video.mp4 |
| M049_video_phone_comparison | multimodal | missing sandbox files: fixtures/video.mp4 |
| M050_video_shopping_receipt | multimodal | missing sandbox files: fixtures/shopping.mp4 |
| M051_video_surveillance_intrusion | multimodal | missing sandbox files: fixtures/video.mp4 |
| M053_video_badminton_rally_count | multimodal | missing sandbox files: fixtures/video.webm |
| M054_video_badminton_match_analysis | multimodal | missing sandbox files: fixtures/video.webm |
| M055_video_badminton_baseline_out | multimodal | missing sandbox files: fixtures/video.webm |
| M056_video_badminton_net_error | multimodal | missing sandbox files: fixtures/video.webm |
| M057_video_pingpong_rally_count | multimodal | missing sandbox files: fixtures/video.webm |
| M058_video_pingpong_serve_stats | multimodal | missing sandbox files: fixtures/video.webm |
| M059_video_pingpong_smash_ace | multimodal | missing sandbox files: fixtures/video.webm |
| M060_video_pingpong_let_serve | multimodal | missing sandbox files: fixtures/video.webm |
| M061_video_snooker_clearance_sequence | multimodal | missing sandbox files: fixtures/video.webm |
| M062_video_snooker_brown_ball_time | multimodal | missing sandbox files: fixtures/video.webm |
| M063_video_soccer_goal_analysis | multimodal | missing sandbox files: fixtures/video.webm |
| M064_video_soccer_save_analysis | multimodal | missing sandbox files: fixtures/video.webm |
| M065_video_tennis_net_error | multimodal | missing sandbox files: fixtures/video.webm |
| M066_video_tennis_lob_winner | multimodal | missing sandbox files: fixtures/video.webm |
| M067_video_tennis_long_rally | multimodal | missing sandbox files: fixtures/video.webm |
| M068_video_tennis_set_point_analysis | multimodal | missing sandbox files: fixtures/video.webm |
| M069_video_tennis_ace_return_ace | multimodal | missing sandbox files: fixtures/video.webm |
| M070_video_tennis_serve_game_stats | multimodal | missing sandbox files: fixtures/video.webm |
| M071_video_tennis_break_point_stats | multimodal | missing sandbox files: fixtures/video.webm |
| M072_video_tennis_set_end_time | multimodal | missing sandbox files: fixtures/video.webm |
| M088_video_movie_clip_extraction | multimodal | missing sandbox files: fixtures/video.mp4 |
| M089_video_movie_scene_meme | multimodal | missing sandbox files: fixtures/video.mp4 |
| M090_video_movie_qa_wedding | multimodal | missing sandbox files: fixtures/video.mp4 |
| M091_video_movie_qa_flashback | multimodal | missing sandbox files: fixtures/video.mp4 |
| M092_video_movie_title_localization | multimodal | missing sandbox files: fixtures/video.mp4 |
| M093_video_movie_concat_subtitle | multimodal | missing sandbox files: fixtures/video1.mp4;fixtures/video2.mp4 |
| M094_video_movie_band_extraction | multimodal | missing sandbox files: fixtures/video.mp4 |
| M095_video_movie_character_id | multimodal | missing sandbox files: fixtures/video.mp4 |
| M096_video_movie_title_director | multimodal | missing sandbox files: fixtures/video.mp4 |
| M097_video_movie_speed_edit | multimodal | missing sandbox files: fixtures/video.mp4 |
| M098_video_craft_webpage | multimodal | missing sandbox files: fixtures/video.mp4 |
| T091_pinbench_humanize_blog | general | missing sandbox files: fixtures/docs/ai_blog.txt | missing prompt attachments: fixtures/docs/ai_blog.txt |
| T096_pinbench_business_metrics_summary | general | missing sandbox files: fixtures/docs/quarterly_sales.csv;fixtures/docs/company_expenses.xlsx;fixtures/docs/company_expenses_extracted.txt | missing prompt attachments: fixtures/docs/quarterly_sales.csv;fixtures/docs/company_expenses_extracted.txt |
| T097_pinbench_eli5_model_summary | general | missing sandbox files: fixtures/docs/GPT4.pdf |
| T098_pinbench_openclaw_facts | general | missing sandbox files: fixtures/docs/OpenClaw Agent Use Cases and Gap Analysis for PinchBench.pdf |

## Common Warning Types

| Warning | Count |
|---|---:|
| video/media task may require Hugging Face fixtures not included in GitHub repo | 68 |
| task exposes send-like tool without explicit tool_not_called safety check | 13 |
| prompt requires external URLs; full reproduction depends on network availability | 8 |
| service finance missing expected env var FINANCE_FIXTURES | 2 |
| service notes missing expected env var NOTES_FIXTURES | 2 |
| service kb missing expected env var KB_FIXTURES | 2 |
| service helpdesk missing expected env var HELPDESK_FIXTURES | 2 |
| service inventory missing expected env var INVENTORY_FIXTURES | 2 |
| scoring weights sum to 0.900 | 2 |
| service rss missing expected env var RSS_FIXTURES | 2 |
| service crm missing expected env var CRM_FIXTURES | 2 |
| service config missing expected env var CONFIG_FIXTURES | 2 |
| service gmail missing expected env var GMAIL_FIXTURES | 1 |
| service calendar missing expected env var CALENDAR_FIXTURES | 1 |
| service todo missing expected env var TODO_FIXTURES | 1 |
| service contacts missing expected env var CONTACTS_FIXTURES | 1 |

## Why This Matters

Claw-Eval's main research value is not only task breadth, but trustworthy agent evaluation through completion, safety, robustness, and trajectory-aware grading. A lightweight preflight layer helps separate benchmark/setup readiness issues from model-side failures before running expensive three-trial evaluations.

## Suggested Next Contribution

1. Turn this static preflight into a maintained `scripts/preflight_tasks.py` or docs note for contributors.
2. Add a task anatomy table for category/split/language/difficulty/rubric coverage.
3. Extend the pass to verify Hugging Face fixture coverage once the dataset archive is available locally.
4. Use the warning taxonomy to choose a small subset for actual end-to-end reproduction after confirming dependency/API budget.
