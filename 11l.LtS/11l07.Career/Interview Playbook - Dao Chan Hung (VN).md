# Kịch Bản Phỏng Vấn — Đào Chấn Hưng (Ethan)

> **Vị trí**: AI/Frontend Engineer  
> **CV**: `19z.Resources/Cv_Dao_Chan_Hung_FE.pdf`  
> **Dự đoán hướng**: Nghiêng về Track 2. Chuyển sang Track 1 nếu phần WebMeet thể hiện được tư duy kiến trúc.  
> **Ngày**: 2026-06-29

---

## Trước buổi phỏng vấn

- [ ] Kiểm tra xem ứng viên có tìm hiểu về công ty trước không (chỉ báo Proactiveness)
- [ ] Lưu ý: Mục AI tooling trong CV có thể là padding — thử thách trực tiếp

---

## Bộ câu hỏi

### Q1 — Router (~5-7 phút)

> **"Walk me through a system you designed or built."** *(Dẫn dắt ứng viên mô tả một hệ thống họ đã thiết kế/xây dựng)*

Nếu không tự chọn, gợi ý: *"You mentioned WebMeet on your CV — tell me about that one."*

**Quy tắc rẽ nhánh:** Có giải thích được *tại sao* (Chime thay vì WebRTC, tradeoff, quyết định về seam)? Nếu có → Track 1. Nếu chỉ mô tả *cái gì* → tiếp tục Track 2 bên dưới.

**Thang câu hỏi đuổi** (chỉ dùng bậc tiếp theo nếu ứng viên chưa tự nói — dừng khi đã có đủ tín hiệu):

| Bậc | Câu hỏi đuổi | Góc nhìn riêng cho Ethan |
|------|-------------|-------------------------|
| 1 | "Tại sao bạn cấu trúc nó theo cách đó?" | Anh ấy có giải thích được vị trí Chime SDK, lựa chọn state management, hay chỉ nói "tech lead quyết định"? |
| 2 | "Bạn đã đánh đổi những gì?" | Chime SDK (đầy đủ tính năng, chi phí cao hơn) vs. WebRTC (rẻ hơn, kiểm soát nhiều hơn). Anh ấy có cân nhắc điều này không? |
| 3 | "Alternative nào bạn đã nghiêm túc cân nhắc và từ chối?" | Có nêu được alternative — Agora, Twilio, WebRTC thuần? Nếu không, Decision-Range yếu. |
| 4 | "Điều gì hỏng hoặc gây bất ngờ sau khi build xong?" | WebMeet có screen sharing + media sync — nhiều bề mặt cho failure. "Không có gì hỏng" là red flag. |
| 5 | "Có điều gì bạn sẽ làm khác nếu làm lại bây giờ không?" | Với 5+ năm kinh nghiệm, có tự critique được việc mình làm? Bonus: thay đổi về CI/CD pipeline hoặc state management. |
| 6 | "Bạn tự drive bao nhiêu phần kiến trúc frontend, so với được giao spec?" | Anh ấy dẫn dắt quyết định stack, hay chỉ là người implement trong team 5 người? |

**Bậc 0** (không cần câu đuổi nào) = ứng viên tự nói được *tại sao*, *tradeoff*, *cái gì hỏng* → tín hiệu Proactiveness + Systems Thinking mạnh. Lãnh thổ Track 1.

---

### Q2 — Critical Thinking Gate (~8-10 phút)

**Phần 1:**
> *"Nhóm của bạn đang xây dựng một AI assistant cho Pochi wallet — chatbot giúp người dùng hiểu giao dịch, giải thích gas fees, trả lời câu hỏi về số dư. PM nói: 'cứ kết nối với LLM rồi ship thôi — không cần filter, nó chỉ giải thích chứ không tư vấn tài chính.' Bạn thấy có gì đáng lo không?"*

| Cần lắng nghe | Đánh giá |
|---------------|----------|
| Nêu được: rủi ro hallucination, prompt injection, lộ PII (địa chỉ ví/số dư), regulatory, "chỉ giải thích" vẫn là ngữ cảnh tài chính | **Đạt** |
| Nêu 1-2 rủi ro chung chung | Ranh giới |
| Đồng ý với PM, không có lo ngại gì | **Trượt** |

**Phần 2:**
> *"Còn 2 tiếng nữa là demo. AI coding agent của bạn — Cursor, tool bạn đang dùng — sinh ra 200 dòng code triển khai chatbot này trong Pochi app. Bạn kiểm tra những gì trước khi mở PR? Dẫn mình qua quy trình của bạn."*

| Cần lắng nghe | Đánh giá |
|---------------|----------|
| Kiểm tra cụ thể: input sanitization, output validation, adversarial test cases, error handling, báo rủi ro cho PM | **Đạt** |
| "Tôi review code, test happy path" — chung chung | Ranh giới |
| "Tôi accept nếu trông ổn" hoặc "Tôi tin Cursor" | **Trượt** |

---

### Q3 — Adaptability (~3-5 phút)

> *"Quay lại WebMeet. Khách hàng US vừa họp, 3 khách enterprise nói họ không dùng được platform vì thiếu real-time captions — một số thành viên bị khiếm thính hoặc không phải người bản ngữ. Họ muốn có trong bản release tới. Bạn đang mid-sprint, chưa ai trong team từng làm captioning. Bạn làm gì?"*

| Cần lắng nghe | Tín hiệu |
|---------------|----------|
| Kiểm tra Chime SDK có built-in transcription không, prototype Web Speech API cho MVP, nêu rõ latency/cost, scope thực tế | **Mạnh** |
| Nghiên cứu API, ước lượng effort, đưa vào sprint planning | Đạt yêu cầu |
| "Chưa từng làm captioning — để người khác làm" | Yếu |

---

### Q4 — Proactiveness (~5-7 phút)

> *"Nhìn lại các dự án — WebMeet, Pochi, Kikan — kể cho mình về một feature hoặc phần việc bạn làm chủ end-to-end. Thứ bạn tự thúc đẩy từ ý tưởng đến delivery, không chỉ nhặt ticket về làm."*

| Cần lắng nghe | Tín hiệu |
|---------------|----------|
| Nêu kết quả cụ thể, mô tả việc ngoài code (thuyết phục PM, scope, deployment), thể hiện ownership rõ ràng | **Mạnh** |
| Nêu một feature đã drive trong phạm vi của mình, rõ ràng nhưng giới hạn | Đạt yêu cầu |
| Chỉ mô tả ticket được assign, ngôn ngữ cộng tác, không có câu chuyện "tôi tự drive" | Yếu |

---

### Q5 — Confidence (~3-5 phút)

> *"Bạn liệt kê AI-assisted engineering là kỹ năng — Cursor, Copilot, MCP, AI agents. Nhưng mô tả dự án của bạn đọc như frontend development tiêu chuẩn. Nếu mình là khách hàng đánh giá team bạn, mình sẽ tự hỏi: AI thực sự thay đổi cách bạn làm việc ở đâu? Dẫn mình qua đi."*

| Cần lắng nghe | Tín hiệu |
|---------------|----------|
| Ví dụ workflow cụ thể với thời gian tiết kiệm thực tế, thừa nhận human judgment vẫn là trung tâm, không phòng thủ | **Mạnh** |
| "Nó giúp nhanh hơn" — chung chung, không phòng thủ nhưng nông | Đạt yêu cầu |
| Phòng thủ, câu trả lời marketing không có nội dung thực | Yếu |

---

### Q6 — Optional A: Curiosity Velocity (~3-5 phút)

> *"Bạn nói có nghiên cứu về AI-assisted workflows — Cursor, MCP, AI agents. Điều thú vị nhất bạn học được trong 6 tháng qua là gì — thứ bạn tự tìm hiểu, không phải được giao? Và bạn đã làm gì với nó?"*

Dùng nếu ứng viên đạt Critical Thinking nhưng nông ở các phần khác. Kiểm tra động lực nội tại.

---

### Q7 — Optional B: Scrappiness (~3-5 phút)

> *"Kể về một lần bạn phải delivery thứ gì đó với quá ít thời gian, quá ít thông tin, hoặc cả hai. Có thể là một feature của Pochi với deadline dApp Store gấp. Bạn đã làm gì — và nếu có thêm thời gian bạn sẽ làm khác điều gì?"*

Dùng nếu ứng viên có tiềm năng nhưng thiếu chiều sâu ở phần khác. Kiểm tra resourcefulness + self-critique.

---

## Phán quyết

| Gate | Kết quả |
|------|---------|
| Critical Thinking | ĐẠT / TRƯỢT |
| Adaptability | Mạnh / Đạt / Yếu |
| Proactiveness | Mạnh / Đạt / Yếu |
| Confidence | Mạnh / Đạt / Yếu |

| Quy tắc quyết định |
|---------------------|
| Đạt Critical Thinking + 2+ Mạnh | **Nhận** |
| Đạt Critical Thinking + 1 Mạnh, còn lại Đạt | **Nhận kèm dè dặt** |
| Trượt Critical Thinking | **Không nhận** |

---

## Track 1 dự phòng (nếu router đạt → chuyển sang đây)

| Đầu dò | Câu hỏi (neo vào WebMeet) |
|--------|---------------------------|
| Depth | "Khó khăn kỹ thuật lớn nhất trong WebMeet là gì?" |
| Proactiveness | "Bạn tự drive bao nhiêu phần kiến trúc frontend, so với được giao spec?" |
| Decision-Range | "Bạn dùng Chime SDK. Alternative nào bạn đã cân nhắc nghiêm túc — WebRTC, Twilio? Tại sao chọn Chime?" |
| Openness | "Kể về một lần bạn push back khách hàng US — thứ họ muốn mà bạn nghĩ là sai." |
| Confidence | "Mình là CTO hoài nghi. Mình nghĩ dùng Chime SDK cho WebMeet là overkill — WebRTC với signaling server rẻ và đơn giản hơn. Thuyết phục mình đi." |
| Adaptability | "Ràng buộc mới: WebMeet cần 500 người concurrent mỗi meeting, không phải 50. Cái gì hỏng trước trong frontend của bạn?" |

---

## Liên quan

- [[candidate-evaluation-rubric]]
- [[ai-engineer-interview-protocol]]
- [[Hypothetical Scenario Menu for Technical Interviews]]
- [[Track 2 Interviewer Reference]]
