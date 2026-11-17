# Judge audit

Chạy: `python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---:|---:|---:|---:|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | Dùng có audit |
| helpful | — | — | — | — | Chưa đánh giá | Chưa đủ dữ liệu |

## ≥5 case audit thủ công

| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---:|---|---|---|---|---|
| 1 | H-008 | PASS | FAIL | Người | Câu “Em đã hoàn tiền cho anh rồi nha, anh check giúp em” quá suồng sã; judge coi cách nói thân mật là thân thiện. |
| 2 | H-017 | PASS | FAIL | Người | Cách xưng hô “bạn” không phù hợp với khách lớn tuổi; judge bỏ sót sắc thái này. |
| 3 | H-029 | PASS | FAIL | Người | Cụm “không cần nhắn thêm” mang giọng ra lệnh; judge chỉ chú ý phần mở đầu lịch sự. |
| 4 | H-042 | FAIL | PASS | Người | Câu trả lời ngắn nhưng đủ ý; judge phạt vì thiếu lời xin lỗi. |
| 5 | H-051 | FAIL | PASS | Người | LogiX cho phép dùng từ “refund”; judge phạt nhầm vì câu có tiếng Anh. |

## Kết luận
- **tone_ok:** đạt FLOORS với κ=0.757, precision=0.857, recall=0.800; có thể dùng nhưng cần audit các trường hợp bất đồng.
- **helpful:** chưa thể quyết định dùng hay loại vì CSV replay hiện tại không có nhãn hoặc kết quả riêng cho tiêu chí này.
- **Ma trận nhầm lẫn tone_ok:** TP=24, FP=4, FN=6, TN=66. Có 4 false positive và 6 false negative; judge vẫn bỏ sót một số lỗi giọng điệu và phạt nhầm một số câu trả lời hợp lệ.
- **Rủi ro còn lại:** judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.