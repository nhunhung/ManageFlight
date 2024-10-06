document.addEventListener('click', function (event) {
    if (event.target.classList.contains('toggle-details')) {
        var flightId = event.target.getAttribute('data-flight-id');
        var classId = event.target.getAttribute('data-class-id');

        // Sử dụng flightId và classId để xác định chi tiết của vé
        console.log('Đã nhấn Xem chi tiết cho chuyến bay ID:', flightId, '- Class ID:', classId);

        // Thêm logic của bạn để hiển thị/ẩn chi tiết hoặc thực hiện bất kỳ hành động nào khác dựa trên dữ liệu
    }
});