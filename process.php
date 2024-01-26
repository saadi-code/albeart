<?php
if (isset($_POST['submit'])) {
    $uploadDir = 'uploads/';
    $uploadFile = $uploadDir . basename($_FILES['pdfFile']['name']);
    $fileType = strtolower(pathinfo($uploadFile, PATHINFO_EXTENSION));

    // Check if the file is a PDF
    if ($fileType != 'pdf') {
        echo 'Only PDF files are allowed.';
        exit;
    }

    // Create the target directory if it doesn't exist
    if (!file_exists($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    // Move the uploaded file to the specified directory
    if (move_uploaded_file($_FILES['pdfFile']['tmp_name'], $uploadFile)) {
        // Call the Python script with the file path
        $pythonScript = '/script.py';
        $command = "python3 $pythonScript $uploadFile";
        $output = shell_exec($command);

        // Display the Python script output
        echo '<h2>Python Script Output:</h2>';
        echo '<pre>' . $output . '</pre>';
    } else {
        echo 'Error uploading file.';
    }
}
?>
