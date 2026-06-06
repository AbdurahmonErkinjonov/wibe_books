from books.models import Category, Book

# Demo kategoriyalar
cats = []
cat_data = [
    ('Klassik Adabiyot', "O'zbek va jahon klassik asarlari"),
    ('Ilm-Fan', "Texnologiya, matematika va fanlar"),
    ('Shaxsiy Rivojlanish', "O'z-o'zini rivojlantirish kitoblari"),
    ('Tarix', "O'zbek va jahon tarixi"),
    ('Bolalar', "Bolalar uchun kitoblar"),
]
for name, desc in cat_data:
    c, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
    cats.append(c)

# Demo kitoblar
books_data = [
    ("O'tkan kunlar", "Abdulla Qodiriy", 35000, "O'zbekiston klassik adabiyotining eng yirik asari.", 408, "O'zbek", 1925, cats[0]),
    ("Atomic Habits", "James Clear", 65000, "Kichik o'zgarishlar, katta natijalar.", 320, "O'zbek tarjima", 2018, cats[2]),
    ("Python dasturlash", "Eric Matthes", 75000, "Pythonni noldan o'rganish.", 560, "O'zbek", 2022, cats[1]),
]
for t,a,p,d,pg,l,y,c in books_data:
    Book.objects.get_or_create(title=t, defaults=dict(author=a,price=p,description=d,pages=pg,language=l,published_year=y,category=c))

print(f"✅ {Category.objects.count()} kategoriya, {Book.objects.count()} kitob")
