FORM_PAGE_HTML = """
<html>
<head>
    <title>Teste</title>
</head>
<body>
<form method="post">
    <input type="hidden" name="csrf" value="bee7aceb836fdbc198fb80a119135a74b0114746ed8d8a5166aabcb9360192f6">
    <div>
        <label for="codigo">Código</label>
    </div>
    <div>
        <input type="text" name="codigo" id="codigo">
    </div>
    <div>
        <input type="submit"></input>
    </div>
    </form>
</body>
</html>
"""

EMPTY_FILE_LIST_PAGE_HTML = """
<html>
<head>
</head>
<body>

</body>
</html>
"""

FILE_LIST_PAGE_HTML = """
<html>
<head>
    <title>Teste - arquivos 98465</title>
</head>
<body>
<div>
    98465</div>
<br><br>
<div>
    <div>Arquivo 1</div>
    <div><a href="arquivo1-98465.txt" download>arquivo.txt</a></div>
    <div><a href="arquivo1-98465.pdf" download>arquivo.pdf</a></div>
</div>
<br><br>
<div>
    <div>Arquivo 2</div>
    <div><a href="arquivo2-98465.txt" download>arquivo2.txt</a></div>
    <div><a href="arquivo2-98465.pdf" download>arquivo2.pdf</a></div>
</div>
</body>
</html>
"""
