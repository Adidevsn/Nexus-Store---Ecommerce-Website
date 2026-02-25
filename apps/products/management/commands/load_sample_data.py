"""
Management command to load sample data for NEXUS STORE.
Run: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from apps.products.models import Category, Product


CATEGORIES = [
    {"name": "Electronics",  "slug": "electronics",  "description": "Cutting-edge tech and gadgets"},
    {"name": "Clothing",     "slug": "clothing",     "description": "Futuristic fashion"},
    {"name": "Footwear",     "slug": "footwear",     "description": "Next-gen kicks"},
    {"name": "Accessories",  "slug": "accessories",  "description": "Complete your look"},
    {"name": "Tech Gear",    "slug": "tech-gear",    "description": "Tools for the future"},
]

PRODUCTS = [
    # Electronics
    {"name": "Quantum Earbuds Pro", "slug": "quantum-earbuds-pro", "category": "electronics", "description": "Next-generation wireless earbuds with neural audio processing and 40-hour battery life.", "price": "199.99", "sale_price": "149.99", "stock": 50, "is_featured": True},
    {"name": "HoloDisplay Monitor", "slug": "holodisplay-monitor", "category": "electronics", "description": "27-inch 4K OLED monitor with 240Hz refresh rate and holographic edge lighting.", "price": "899.00", "stock": 12, "is_featured": True},
    {"name": "Neural Smartwatch X", "slug": "neural-smartwatch-x", "category": "electronics", "description": "Advanced health monitoring smartwatch with biometric scanning and 7-day battery.", "price": "349.00", "sale_price": "279.00", "stock": 35, "is_featured": False},
    {"name": "Compact Drone V2", "slug": "compact-drone-v2", "category": "electronics", "description": "Foldable 4K drone with 30-minute flight time and obstacle avoidance AI.", "price": "449.00", "stock": 8, "is_featured": True},

    # Clothing
    {"name": "Void Jacket — Matte Black", "slug": "void-jacket-matte-black", "category": "clothing", "description": "Ultra-lightweight thermally adaptive jacket with integrated LED accent strips.", "price": "249.00", "stock": 20, "is_featured": True},
    {"name": "Phantom Hoodie", "slug": "phantom-hoodie", "category": "clothing", "description": "Premium cotton hoodie with embossed hex pattern and deep kangaroo pockets.", "price": "89.00", "sale_price": "65.00", "stock": 45, "is_featured": False},
    {"name": "Nexus Cargo Pants", "slug": "nexus-cargo-pants", "category": "clothing", "description": "Tactical cargo pants with 8 pockets, stretch fabric, and water resistance.", "price": "119.00", "stock": 30, "is_featured": False},

    # Footwear
    {"name": "Stealth Runner X1", "slug": "stealth-runner-x1", "category": "footwear", "description": "Minimalist performance running shoes with carbon fiber sole and reactive cushioning.", "price": "189.00", "sale_price": "139.00", "stock": 25, "is_featured": True},
    {"name": "Cyber Boot — Chrome", "slug": "cyber-boot-chrome", "category": "footwear", "description": "Platform boots with metallic chrome finish and anti-gravity foam insole.", "price": "219.00", "stock": 15, "is_featured": False},
    {"name": "Grid Sneaker Low", "slug": "grid-sneaker-low", "category": "footwear", "description": "Low-profile sneakers with laser-cut grid pattern and breathable mesh upper.", "price": "129.00", "stock": 40, "is_featured": False},

    # Accessories
    {"name": "Prismatic Backpack 25L", "slug": "prismatic-backpack-25l", "category": "accessories", "description": "Water-resistant backpack with color-shifting fabric and laptop sleeve.", "price": "149.00", "sale_price": "119.00", "stock": 18, "is_featured": True},
    {"name": "Signal Ring — Titanium", "slug": "signal-ring-titanium", "category": "accessories", "description": "NFC-enabled titanium ring for contactless payments and device access.", "price": "79.00", "stock": 60, "is_featured": False},
    {"name": "Neon Beanie", "slug": "neon-beanie", "category": "accessories", "description": "Warm merino wool beanie with subtle reactive fiber that glows under UV light.", "price": "39.00", "stock": 0, "is_featured": False},

    # Tech Gear
    {"name": "Portable Power Hub", "slug": "portable-power-hub", "category": "tech-gear", "description": "20,000mAh power bank with 6 ports, wireless charging, and solar backup panel.", "price": "119.00", "stock": 22, "is_featured": False},
    {"name": "Pixel Mechanical Keyboard", "slug": "pixel-mechanical-keyboard", "category": "tech-gear", "description": "Compact TKL mechanical keyboard with per-key RGB and custom linear switches.", "price": "179.00", "sale_price": "149.00", "stock": 14, "is_featured": True},
]


class Command(BaseCommand):
    help = 'Load sample data for NEXUS STORE'

    def handle(self, *args, **options):
        self.stdout.write('Loading categories...')
        category_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'description': cat_data['description']}
            )
            category_map[cat_data['slug']] = cat
            status = 'created' if created else 'exists'
            self.stdout.write(f'  [{status}] {cat.name}')

        self.stdout.write('Loading products...')
        for p_data in PRODUCTS:
            cat = category_map.get(p_data.pop('category'))
            slug = p_data['slug']
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={**p_data, 'category': cat}
            )
            status = 'created' if created else 'exists'
            self.stdout.write(f'  [{status}] {product.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Done! {Category.objects.count()} categories, {Product.objects.count()} products loaded.'
        ))
        self.stdout.write(self.style.WARNING(
            '\nNote: Product images must be added via the admin panel (/admin/)\n'
        ))
