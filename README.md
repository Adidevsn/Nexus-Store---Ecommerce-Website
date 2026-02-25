# Nexus-Store---Ecommerce-Website
⬡ NEXUS STORE

A fully functional dark-themed ecommerce web app built with Django 4.2 as a 3rd year CSE project.

NEXUS STORE is a complete end-to-end ecommerce platform — from browsing products and managing a cart, to checking out with Stripe and tracking orders. The UI is futuristic and dark, built with glassmorphism cards, neon cyan accents, glitch animations, and premium typography. Everything is 100% Python fullstack — no React, no Node, no build tools.

✨ Features
🛒 Shopping Experience

Product catalog with pagination, search, category filtering, and sort by price or date
Product detail pages with stock indicators, quantity selector, and related products
Session-based shopping cart — no login required, persists for 7 days
Checkout form with shipping address pre-filled from user profile
Stripe Checkout integration — users are redirected to Stripe's hosted page, no card data touches your server
Stock automatically decrements after a successful order

👤 User Accounts

Register, login, logout using Django's built-in authentication
Profile page with avatar, phone number, address, and city
Edit profile and change password
View recent orders directly from the profile page

📦 Orders

Auto-generated order numbers in NX-XXXXXXXX format
Order history page listing all past purchases
Detailed order page with item breakdown, shipping address, and payment status
Visual status timeline: Pending → Confirmed → Shipped → Delivered

🛠 Admin Panel

Django admin with the Jazzmin darkly theme — looks professional out of the box
Inline order items inside order records
Bulk-editable product fields (price, stock, active, featured)
load_sample_data management command seeds 5 categories and 15 products instantly

