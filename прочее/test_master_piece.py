from pymystem3 import Mystem

text = "Красивая мама красиво мыла раму"
m = Mystem()
lemmas = m.analyze(text)
print(lemmas)