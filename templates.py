MAIN = """
<html>
<body>
<h1>Let's play Madlibs!</h1>
<a href="/madlib"><button>Play Madlibs</button></a>
</body>
</html>
"""

FORM = """
<html>
<body>
<h1>Fill in the blanks!</h1>
<form method="POST" action="/madlib">
{key}
{blanks}
<button type="submit">Submit</button>
</form>
</body>
</html>
"""

MADLIB = """
<html>
<body>
<h1>Here's your madlib!</h1>
<p>{madlib}</p>
<a href="/madlib"><button>Play again!</button></a>
<a href="/"><button>Back to Start</button></a>
</body>
</html>
"""

NOT_FOUND = """
<html>
<body>
<h1>404: Hmm... we couldn't find that one</h1>
<a href="/"><button>Back to Start</button></a>
</body>
</html>
"""
