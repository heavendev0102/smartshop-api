from decimal import Decimal

# Browse By Category (UI grid)
DEFAULT_CATEGORIES = [
    {
        "name": "Phones",
        "slug": "phones",
        "description": "Mobile phones and smartphones",
        "icon_url": "https://placehold.co/64x64/ede9fe/5b21b6?text=Phone",
        "display_order": 1,
    },
    {
        "name": "SmartWatches",
        "slug": "smartwatches",
        "description": "Smart watches and wearables",
        "icon_url": "https://placehold.co/64x64/e0e7ff/312e81?text=Watch",
        "display_order": 2,
    },
    {
        "name": "Cameras",
        "slug": "cameras",
        "description": "Digital cameras and accessories",
        "icon_url": "https://placehold.co/64x64/fef3c7/92400e?text=Camera",
        "display_order": 3,
    },
    {
        "name": "Headphones",
        "slug": "headphones",
        "description": "Headphones and earbuds",
        "icon_url": "https://placehold.co/64x64/f3f4f6/374151?text=Audio",
        "display_order": 4,
    },
    {
        "name": "Computers",
        "slug": "computers",
        "description": "Laptops, tablets, and desktops",
        "icon_url": "https://placehold.co/64x64/f5f5f4/44403c?text=PC",
        "display_order": 5,
    },
    {
        "name": "Gaming",
        "slug": "gaming",
        "description": "Gaming consoles and gear",
        "icon_url": "https://placehold.co/64x64/dcfce7/166534?text=Game",
        "display_order": 6,
    },
]

# Homepage product tabs (not browse categories)
DEFAULT_SECTIONS = [
    {
        "name": "New Arrivals",
        "slug": "new_arrivals",
        "description": "Latest products",
        "display_order": 1,
    },
    {
        "name": "Bestsellers",
        "slug": "bestsellers",
        "description": "Top selling products",
        "display_order": 2,
    },
    {
        "name": "Featured",
        "slug": "featured",
        "description": "Highlighted products",
        "display_order": 3,
    },
]

DUMMY_PRODUCTS = [
    {
        "name": "Apple iPhone 14 Pro Max 128GB Deep Purple",
        "image_url": "https://placehold.co/600x600/ede9fe/5b21b6?text=iPhone+14+Pro",
        "description": "6.7-inch Super Retina XDR display with ProMotion. A16 Bionic chip and 48MP main camera.",
        "stock": 25,
        "ratings": Decimal("4.80"),
        "current_price": Decimal("810.00"),
        "original_price": Decimal("900.00"),
        "discount_percent": 10,
        "category_slugs": ["phones"],
        "section_slugs": ["new_arrivals", "featured"],
    },
    {
        "name": "Apple AirPods Max Over-Ear Headphones - Space Gray",
        "image_url": "https://placehold.co/600x600/f3f4f6/374151?text=AirPods+Max",
        "description": "High-fidelity audio with Active Noise Cancellation and spatial audio.",
        "stock": 40,
        "ratings": Decimal("4.60"),
        "current_price": Decimal("299.00"),
        "original_price": Decimal("599.00"),
        "discount_percent": 50,
        "category_slugs": ["headphones"],
        "section_slugs": ["new_arrivals", "bestsellers"],
    },
    {
        "name": "Samsung Galaxy Watch6 Classic 47mm Black",
        "image_url": "https://placehold.co/600x600/e0e7ff/312e81?text=Galaxy+Watch6",
        "description": "Premium smartwatch with rotating bezel, health tracking, and Wear OS.",
        "stock": 18,
        "ratings": Decimal("4.50"),
        "current_price": Decimal("249.00"),
        "original_price": Decimal("329.00"),
        "discount_percent": 24,
        "category_slugs": ["smartwatches"],
        "section_slugs": ["bestsellers", "featured"],
    },
    {
        "name": "Apple iPad 9 10.2 64GB Wi-Fi Silver (MK2L3) 2021",
        "image_url": "https://placehold.co/600x600/f5f5f4/44403c?text=iPad+9",
        "description": "10.2-inch Retina display, A13 Bionic chip, and support for Apple Pencil (1st gen).",
        "stock": 30,
        "ratings": Decimal("4.70"),
        "current_price": Decimal("279.00"),
        "original_price": Decimal("329.00"),
        "discount_percent": 15,
        "category_slugs": ["computers"],
        "section_slugs": ["new_arrivals", "bestsellers", "featured"],
    },
]
