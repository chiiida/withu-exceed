function doctorSure() {
    var password = prompt("Please enter doctor ID");
    if (password == '12345678') {
        document.getElementById('docPage').href = "doctor.html";
    } else {
        document.getElementById('docPage').href = "#";
    }
  }