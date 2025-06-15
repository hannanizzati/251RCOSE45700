from flask import Flask, render_template, request, jsonify, redirect, url_for 
import random

app = Flask(__name__)

# Event data
events = [
    {
        "id": 1,
        "name": "2NE1 - 2024 CONCERT IN SEOUL",
        "date": "2024-11-28",
        "price": "₩165,000",
        "genre": "POP",
        "location": "Seoul",
        "segments": {
            "VVIP": {"price": "₩300,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩200,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩100,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
    {
        "id": 2,
        "name": "KESHI - WORLD TOUR",
        "date": "2024-11-25",
        "price": "₩150,000",
        "genre": "POP",
        "location": "Seoul",
        "segments": {
            "VVIP": {"price": "₩280,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩180,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩90,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
    {
        "id": 3,
        "name": "COLDPLAY - MUSIC OF THE SPHERES",
        "date": "2024-12-10",
        "price": "₩200,000",
        "genre": "POP",
        "location": "Seoul",
        "segments": {
            "VVIP": {"price": "₩350,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩250,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩120,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
    {
        "id": 4,
        "name": "Kinky Boots",
        "date": "2024-11-28",
        "price": "₩90,000",
        "genre": "MUSICAL",
        "location": "Seoul",
        "segments": {
            "VVIP": {"price": "₩180,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩120,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩60,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
    {
        "id": 5,
        "name": "Epik High – 2024 Concert",
        "date": "2024-12-20",
        "price": "₩120,000",
        "genre": "VOCAL",
        "location": "Olympic Park Handball Gymnasium",
        "segments": {
            "VVIP": {"price": "₩250,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩180,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩100,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
    {
        "id": 6,
        "name": "Jannabi – 'Fantastic Old Fashioned 2024: Movie Star Rising'",
        "date": "2024-09-01",
        "price": "₩100,000",
        "genre": "FOLK",
        "location": "Seoul",
        "segments": {
            "VVIP": {"price": "₩200,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩150,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩80,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
    {
        "id": 7,
        "name": "Jannabi – 'Fantastic Old Fashioned 2024: Movie Star Rising'",
        "date": "2024-09-14",
        "price": "₩100,000",
        "genre": "FOLK",
        "location": "Busan",
        "segments": {
            "VVIP": {"price": "₩200,000", "seats": {f"A{i}": "available" for i in range(1, 11)}},
            "VIP": {"price": "₩150,000", "seats": {f"B{i}": "available" for i in range(1, 16)}},
            "Regular": {"price": "₩80,000", "seats": {f"C{i}": "available" for i in range(1, 21)}},
        },
    },
]

# List of reservations (to be saved in-memory for simplicity)
reservations_list = []

@app.route("/")
def home():
    # Explicitly select 2NE1, Keshi, and Coldplay for recommendations
    recommended_events = [
        event for event in events if event["name"] in [
            "2NE1 - 2024 CONCERT IN SEOUL", 
            "KESHI - WORLD TOUR", 
            "COLDPLAY - MUSIC OF THE SPHERES"
        ]
    ]
    # Add image paths for these events
    for event in recommended_events:
        event["image"] = f"images/{event['id']}.jpg"  # Images named based on event IDs

    return render_template("index.html", events=events, recommended_events=recommended_events)

# Genre filter route
@app.route("/genre/<genre>")
def genre(genre):
    filtered_events = [event for event in events if event["genre"].lower() == genre.lower()]
    return render_template("genre.html", genre=genre, events=filtered_events)

# Search route
@app.route("/search", methods=["GET"])
def search_events():
    keyword = request.args.get("keyword", "").lower()
    location = request.args.get("location", "").lower()
    date = request.args.get("date", "")

    filtered_events = [
        event
        for event in events
        if (keyword in event["name"].lower())
        and (location in event["location"].lower() if location else True)
        and (date <= event["date"] if date else True)
    ]

    return render_template("events.html", events=filtered_events)

# Event details route
@app.route('/details/<int:event_id>')
def event_details(event_id):
    event = next((event for event in events if event["id"] == event_id), None)
    if event:
        return render_template("details.html", event=event)
    else:
        return "Event not found", 404

# Seat map route
@app.route("/seat_map/<int:event_id>")
def seat_map(event_id):
    event = next((event for event in events if event["id"] == event_id), None)
    seats_limit = int(request.args.get("seats", 1))
    if event:
        return render_template("seat_map.html", event=event, seats_limit=seats_limit)
    return "Event not found", 404

# Reserve seats route
@app.route("/reserve_seats/<int:event_id>", methods=["POST"])
def reserve_seats(event_id):
    event = next((event for event in events if event["id"] == event_id), None)
    if not event:
        return jsonify({"success": False, "error": "Event not found"})

    selected_seats = request.json.get("seats", [])
    for segment, data in event["segments"].items():
        for seat in selected_seats:
            if seat in data["seats"] and data["seats"][seat] == "available":
                data["seats"][seat] = "reserved"

    return jsonify({"success": True})

# Confirm order route
@app.route("/confirm_order_page/<int:event_id>")
def confirm_order_page(event_id):
    event = next((event for event in events if event["id"] == event_id), None)
    if not event:
        return "Event not found", 404

    seats = request.args.get("seats", "").split(",")
    buyer_name = request.args.get("buyer_name")
    buyer_email = request.args.get("buyer_email")
    buyer_contact = request.args.get("buyer_contact")

    total_price = 0
    reserved_seats = []

    for segment, data in event["segments"].items():
        for seat in seats:
            if seat in data["seats"]:
                reserved_seats.append({"segment": segment, "seat": seat, "price": data["price"]})
                total_price += int(data["price"].replace("₩", "").replace(",", ""))

    return render_template(
        "confirm_order.html",
        event=event,
        reserved_seats=reserved_seats,
        total_price=f"₩{total_price:,}",
        buyer_name=buyer_name,
        buyer_email=buyer_email,
        buyer_contact=buyer_contact
    )

# Payment route
@app.route("/payment/<int:event_id>", methods=["POST"])
def payment(event_id):
    event = next((event for event in events if event["id"] == event_id), None)
    if not event:
        return "Event not found", 404

    # Get user input from the form
    buyer_name = request.form.get("buyer_name")
    buyer_email = request.form.get("buyer_email")
    buyer_contact = request.form.get("buyer_contact")
    seats = request.form.get("seats")

    # Validate required fields
    if not all([buyer_name, buyer_email, buyer_contact, seats]):
        return "Invalid details. Please complete the form.", 400

    # Display the payment page
    return render_template(
        "payment.html",
        event=event,
        buyer_name=buyer_name,
        buyer_email=buyer_email,
        buyer_contact=buyer_contact,
        seats=seats,
        success=False,
    )

# Complete purchase route
@app.route("/complete_purchase/<int:event_id>", methods=["POST"])
def complete_purchase(event_id):
    event = next((event for event in events if event["id"] == event_id), None)
    if not event:
        return "Event not found", 404

    buyer_name = request.form.get("buyer_name")
    buyer_email = request.form.get("buyer_email")
    buyer_contact = request.form.get("buyer_contact")
    seats = request.form.get("seats").split(",")  # Ensure seats are split into a list

    # Generate an order number
    order_number = random.randint(100000, 999999)

    # Calculate total price and reserved seats
    total_price = 0
    reserved_seats = []
    for segment, data in event["segments"].items():
        for seat in seats:
            if seat in data["seats"]:
                reserved_seats.append(seat)
                total_price += int(data["price"].replace("₩", "").replace(",", ""))

    # Add to reservations_list
    global reservations_list
    reservations_list.append({
        "order_number": order_number,
        "event": event["name"],
        "location": event["location"],
        "buyer_name": buyer_name,
        "buyer_email": buyer_email,
        "buyer_contact": buyer_contact,
        "seats": reserved_seats,
        "total_price": total_price,
    })

    return render_template(
        "success.html",
        event=event,
        buyer_name=buyer_name,
        buyer_email=buyer_email,
        buyer_contact=buyer_contact,
        order_number=order_number,
        total_price=total_price,
        reserved_seats=reserved_seats
    )

# Reservations page
@app.route("/reservations_page")
def reservations():
    return render_template("reservations.html", reservations=reservations_list)

@app.route("/cancel_reservation/<int:order_number>", methods=["POST"])
def cancel_reservation(order_number):
    # Find the reservation to cancel
    reservation = next((res for res in reservations_list if res["order_number"] == order_number), None)
    if not reservation:
        return jsonify({"success": False, "error": "Reservation not found."}), 404

    # Find the event related to the reservation
    event = next((event for event in events if event["name"] == reservation["event"]), None)
    if not event:
        return jsonify({"success": False, "error": "Event not found."}), 404

    # Mark reserved seats as available
    for seat in reservation["seats"]:
        for segment, data in event["segments"].items():
            if seat in data["seats"]:
                data["seats"][seat] = "available"

    # Remove the reservation
    reservations_list.remove(reservation)

    return jsonify({"success": True, "message": "Reservation canceled successfully."})

@app.route("/my_reservations")
def my_reservations():
    return render_template("reservations.html", reservations=reservations_list)


if __name__ == "__main__":
    app.run(debug=True)