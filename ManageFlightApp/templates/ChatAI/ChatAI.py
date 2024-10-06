"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "AIzaSyBBqkoTAc97lewek-wPDiyzGTjVpOGMU-A"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

def chatbot_response(user_message):

  conversation_history = [
    "input: Thời gian bay từ TP.HCM đến Hà Nội là bao lâu?",
    "output: Thời gian bay từ TP.HCM đến Hà Nội là khoảng 8 tiếng.",
    "input: Chuyến bay từ Đà Nẵng đến Hải Phòng có dừng ở đâu không?",
    "output: Chuyến bay từ Đà Nẵng đến Hải Phòng không có điểm dừng.",
    "input: Giá vé hạng phổ thông cho chuyến bay từ Sapa đến Phan Thiết là bao nhiêu?",
    "output: Giá vé hạng phổ thông cho chuyến bay từ Sapa đến Phan Thiết là 1.700.000 VND.",
    "input: Có chuyến bay nào từ Tây Ninh đến Sapa không?",
    "output: Có chuyến bay từ Tây Ninh đến Sapa, thời gian bay khoảng 10 tiếng.",
    "input: Mình có thể đặt vé hạng thương gia cho chuyến bay từ TP.HCM đến Đà Nẵng không?",
    "output: Bạn có thể đặt vé hạng thương gia với giá 3.200.000 VND cho chuyến bay này.",
    "input: Thời gian hạ cánh của chuyến bay từ Vũng Tàu đến Đà Lạt là khi nào?",
    "output: Chuyến bay từ Vũng Tàu đến Đà Lạt sẽ hạ cánh lúc 17:00 ngày 20/01/2024.",
    "input: Có chuyến bay nào từ Đà Lạt đến TP.HCM không?",
    "output: Có chuyến bay từ Đà Lạt đến TP.HCM, khởi hành vào ngày 20/01/2024 lúc 09:00.",
    "input: Địa điểm du lịch nào hot nhất ở Sapa?",
    "output: Fansipan là điểm đến nổi bật nhất ở Sapa.",
    "input: Tôi muốn biết số lượng ghế trống trên chuyến bay VN001?",
    "output: Trên chuyến bay VN001, hiện còn 4 ghế trống.",
    "input: Khoảng cách từ TP.HCM đến Cà Mau là bao nhiêu?",
    "output: Khoảng cách từ TP.HCM đến Cà Mau là 1.190 km.",
    "input: Tôi có thể bay từ Hà Nội đến Đà Nẵng không?",
    "output: Bạn có thể bay từ Hà Nội đến Đà Nẵng qua chuyến bay từ TP.HCM.",
    "input: Chuyến bay từ Đà Nẵng đến Đà Lạt có bao nhiêu điểm dừng?",
    "output: Chuyến bay từ Đà Nẵng đến Đà Lạt không có điểm dừng.",
    "input: Giá vé máy bay từ TP.HCM đến Cà Mau là bao nhiêu?",
    "output: Giá vé hạng phổ thông là 2.500.000 VND và hạng thương gia là 3.500.000 VND.",
    "input: Khi nào có chuyến bay từ Sapa đến Vũng Tàu?",
    "output: Hiện tại không có chuyến bay thẳng từ Sapa đến Vũng Tàu.",
    "input: Có chuyến bay nào khởi hành từ TP.HCM đến Hà Nội vào ngày 31/12/2023 không?",
    "output: Có chuyến bay từ TP.HCM đến Hà Nội khởi hành lúc 02:00 ngày 31/12/2023.",
    "input: Máy bay VN004 có bao nhiêu ghế?",
    "output: Máy bay VN004 có tổng cộng 15 ghế.",
    "input: Máy bay VN001 có ghế hạng thương gia không?",
    "output: Máy bay VN001 có ghế hạng thương gia với giá vé 3.500.000 VND.",
    "input: Có chuyến bay nào đi Phan Thiết vào ngày 20/02/2024 không?",
    "output: Có chuyến bay từ Sapa đến Phan Thiết vào ngày 20/02/2024.",
    "input: Thời gian bay từ Tây Ninh đến Sapa là bao nhiêu?",
    "output: Thời gian bay từ Tây Ninh đến Sapa là khoảng 10 tiếng.",
    "input: Máy bay VN007 có khởi hành từ Hà Nội không?",
    "output: Máy bay VN007 không khởi hành từ Hà Nội.",
    "input: Giá vé máy bay từ TP.HCM đến Đà Nẵng hạng thương gia là bao nhiêu?",
    "output: Giá vé hạng thương gia từ TP.HCM đến Đà Nẵng là 3.200.000 VND.",
    "input: Có chuyến bay nào từ Hải Phòng đến Hà Nội không?",
    "output: Có chuyến bay từ Hải Phòng đến Hà Nội, khoảng cách bay là 400 km.",
    "input: Số ghế trống trên chuyến bay VN002 là bao nhiêu?",
    "output: Hiện tại, chuyến bay VN002 còn 8 ghế trống.",
    "input: Đà Lạt có phải là điểm đến du lịch nổi bật không?",
    "output: Đà Lạt là điểm đến du lịch nổi bật với phong cảnh thiên nhiên tuyệt đẹp.",
    "input: Chuyến bay từ Sapa đến Phan Thiết có ghé qua sân bay nào không?",
    "output: Chuyến bay từ Sapa đến Phan Thiết không ghé qua sân bay nào.",
    "input: Vé hạng thương gia trên chuyến bay từ Vũng Tàu đến Đà Lạt là bao nhiêu?",
    "output: Vé hạng thương gia trên chuyến bay từ Vũng Tàu đến Đà Lạt có giá 3.500.000 VND.",
    "input: Mình muốn bay từ TP.HCM đến Cà Mau, khi nào có chuyến bay?",
    "output: Có chuyến bay từ TP.HCM đến Cà Mau vào ngày 31/01/2024.",
    "input: Có bao nhiêu ghế hạng phổ thông trên chuyến bay VN003?",
    "output: Chuyến bay VN003 có 15 ghế hạng phổ thông.",
    "input: Sân bay tại Đà Nẵng nằm ở đâu?",
    "output: Sân bay tại Đà Nẵng nằm ở Hiệp Phước, Đà Nẵng.",
    "input: Chuyến bay VN001 có ghế trống nào không?",
    "output: Hiện tại chuyến bay VN001 còn ghế trống hạng phổ thông và hạng thương gia.",
    "input: Hãy nói tiếng Việt",
    "output: Tôi có thể nói tiếng Việt",
    "input: Chuyến bay từ Đà Nẵng đến Hải Phòng có dừng ở đâu không?", # Truyền input vào đây, input từ chatbot trên giao diện đã được tạo
    "output: ", #output sẽ được đưa ra
]

  conversation_history[-2] = f"input: {user_message}"

  response = model.generate_content(conversation_history)

  return response.text


user_message = "Chuyến bay từ TP.HCM đến Đà Nẵng có mất nhiều thời gian không?"
response = chatbot_response(user_message)
print(response)