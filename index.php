<!--<!DOCTYPE html>-->
<!--<html lang="en">-->
<!--<head>-->
<!--    <meta charset="UTF-8">-->
<!--    <meta name="viewport" content="width=device-width, initial-scale=1.0">-->
<!--    <title>PDF Processor</title>-->
<!--</head>-->
<!--<body>-->
<!--<h2>Upload PDF File</h2>-->
<!--<form action="process.php" method="post" enctype="multipart/form-data">-->
<!--    <input type="file" name="pdfFile" accept=".pdf" required>-->
<!--    <button type="submit" name="submit">Process PDF</button>-->
<!--</form>-->
<!--</body>-->
<!--</html>-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Processing Form</title>
</head>
<body>
<h1>PDF Processing Form</h1>
<form action="index.php" method="post">
    <label for="pdf_path">PDF Path:</label>
    <input type="text" id="pdf_path" name="pdf_path" required>
    <button type="submit">Process PDF</button>
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $pdf_path = $_POST["pdf_path"];

    // Validate and sanitize the input if needed

    // Call your Python script with the PDF path
    if (!empty($pdf_path)) {
        try {
            $output = shell_exec("python3 script.py " . escapeshellarg($pdf_path));
            echo "<h2>Processing Result</h2>";
            echo "<pre>$output</pre>";
        } catch (Exception $e) {
            echo "<p>Error: {$e->getMessage()}</p>";
        }
    } else {
        echo "<p>PDF path not provided</p>";
    }
}
?>
</body>
</html>
