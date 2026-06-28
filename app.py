import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timezone
from config import get_db

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'quins_secret_rugby_key_1923')

# Mock data for initial rendering
NEWS_ARTICLES = [
    {
        "id": "1",
        "title": "Kenya Harlequin Clinch Thrilling Kenya Cup Victory!",
        "date": "June 18, 2026",
        "summary": "A last-minute penalty try sealed an epic 24-21 victory at the RFUEA Grounds in front of a packed crowd.",
        "content": "An incredible performance from Quins saw us secure a massive victory in the Kenya Cup championship. The atmosphere at the RFUEA Grounds was electric. Down by 5 points with only three minutes left, the forward pack forced a penalty try that sent the stadium into absolute delirium. Head coach praised the team's resilience and mental strength, noting that this victory sets a new benchmark for the rest of the season.",
        "image": "news_match.jpg"
    },
    {
        "id": "2",
        "title": "Christie 7s 2026 Edition: Dates and Ticketing Announced",
        "date": "June 24, 2026",
        "summary": "Africa's oldest and most prestigious club rugby 7s tournament returns this August at the RFUEA Grounds.",
        "content": "We are thrilled to officially announce the dates for the Christie 7s 2026 edition, which will run from August 15th to August 16th. Established in 1964, Christie 7s continues to be the ultimate celebration of rugby, culture, and community. This year's tournament will feature Division 1, Division 2, Women's, Under-16s, and the beloved Golden Oldies veterans' competition. Tickets are now on sale with special early-bird rates.",
        "image": "christie7s.jpg"
    },
    {
        "id": "3",
        "title": "Women's Team Welcomes New Main Sponsor for 2026",
        "date": "May 30, 2026",
        "summary": "The Quins Women's team secures a landmark partnership deal to boost training facilities and travel budgets.",
        "content": "In a major boost for women's rugby in Kenya, the Kenya Harlequins Women's team has officially signed a three-year sponsorship contract. The partnership will fund advanced training camps, professional coaching staff, and international travel. Club management highlighted this as a crucial step towards gender parity and expanding the player pathway for young female athletes.",
        "image": "womens_team.jpg"
    }
]

PLAYERS = {
    "mens": [
        {"name": "Eden Agero", "position": "Fly-half / Captain", "number": "10", "story": "A seasoned veteran of the national team and Quins talisman. Known for exceptional tactical kicking and leadership on the pitch.", "image": "player_eden.jpg"},
        {"name": "Herman Humwa", "position": "Flanker", "number": "7", "story": "A physical powerhouse in both 15s and 7s. Famous for dominant tackles and securing crucial turnovers at the breakdown.", "image": "player_herman.jpg"},
        {"name": "Willy Ambaka", "position": "Winger", "number": "11", "story": "Commonly known as the 'Kenyan Lomu'. His explosive speed and brute strength make him a constant threat on the wing.", "image": "player_willy.jpg"},
        {"name": "Patrice Agunda", "position": "Inside Center", "number": "12", "story": "A defensive rock and experienced playmaker who holds the midfield together with sharp positioning and communication.", "image": "player_patrice.jpg"}
    ],
    "womens": [
        {"name": "Philadelphia Olando", "position": "Center / Captain", "number": "13", "story": "An icon of Kenyan women's rugby. Leads the team with unparalleled experience, tactical intelligence, and physical grit.", "image": "player_philadelphia.jpg"},
        {"name": "Grace Adhiambo", "position": "Fly-half", "number": "10", "story": "A creative maestro whose passing range and quick feet unlock the tightest defenses. Key playmaker for both club and country.", "image": "player_grace.jpg"},
        {"name": "Janet Okello", "position": "Winger", "number": "14", "story": "Nicknamed 'She-scrum', her blistering pace off the mark has left countless defenders in her wake on both the regional and global stage.", "image": "player_janet.jpg"},
        {"name": "Sheila Chajira", "position": "Flanker", "number": "6", "story": "A hard-hitting forward known for work rate, ferocious tackling, and a relentless attitude in contact situations.", "image": "player_sheila.jpg"}
    ]
}

UPCOMING_MATCHES = [
    {"opponent": "Kabras Sugar RFC", "date": "July 04, 2026", "time": "16:00 EAT", "venue": "RFUEA Grounds, Nairobi", "competition": "Kenya Cup"},
    {"opponent": "KCB RC", "date": "July 18, 2026", "time": "15:30 EAT", "venue": "KCB Sports Club, Ruaraka", "competition": "Kenya Cup"},
    {"opponent": "Mwamba RFC", "date": "August 01, 2026", "time": "16:00 EAT", "venue": "RFUEA Grounds, Nairobi", "competition": "Enterprise Cup"}
]

SHOP_ITEMS = [
    {
        "id": "jersey_replica",
        "name": "Official Kenya Harlequin Replica Jersey",
        "price": "KES 5,500",
        "description": "Premium quality polyester featuring the classic Quins colors and quartered design. Breathable fabric suitable for playing or fan support.",
        "image": "jersey_replica.jpg",
        "sizes": ["S", "M", "L", "XL", "XXL", "3XL", "4XL"],
        "options": ["Men's Cut", "Women's Cut"]
    },
    {
        "id": "wristband_quins",
        "name": "Kenya Harlequin Wristband",
        "price": "KES 400",
        "description": "Elastic silicone wristband branded with the club name and colors. Perfect accessory to show your Quins pride.",
        "image": "wristband.jpg",
        "sizes": ["Standard"],
        "options": []
    },
    {
        "id": "merchandise_cap",
        "name": "Quins Branded Snapback Cap",
        "price": "KES 1,800",
        "description": "High-profile structured cap with embroidered Kenya Harlequins badge and premium cotton finish.",
        "image": "snapback.jpg",
        "sizes": ["One Size Fits All"],
        "options": ["Black", "Brown-White Quarters"]
    }
]

SPONSORS = [
    {"name": "SportPesa", "logo_class": "sponsor-sportpesa", "text": "Title Sponsor"},
    {"name": "Safaricom", "logo_class": "sponsor-safaricom", "text": "Official Telecom Partner"},
    {"name": "Kenya Breweries", "logo_class": "sponsor-kbl", "text": "Beverage Partner"},
    {"name": "Mookh", "logo_class": "sponsor-mookh", "text": "Official Ticketing Partner"}
]

# Routes
@app.route('/')
def index():
    return render_template(
        'index.html',
        matches=UPCOMING_MATCHES,
        news=NEWS_ARTICLES[:2], # Show top 2 news articles on homepage
        featured_players=PLAYERS['mens'][:2] + PLAYERS['womens'][:2], # Show some featured players
        title="Home"
    )

@app.route('/news')
def news():
    search_query = request.args.get('q', '').strip().lower()
    filtered_news = NEWS_ARTICLES
    if search_query:
        filtered_news = [
            art for art in NEWS_ARTICLES 
            if search_query in art['title'].lower() or search_query in art['content'].lower()
        ]
    return render_template('news.html', news=filtered_news, search_query=search_query, title="Team News & History")

@app.route('/players')
def players():
    return render_template('players.html', squads=PLAYERS, title="Player Profiles")

@app.route('/fixtures')
def fixtures():
    return render_template('fixtures.html', matches=UPCOMING_MATCHES, title="Fixtures & Results")

@app.route('/shop')
def shop():
    return render_template('shop.html', items=SHOP_ITEMS, title="Official Shop")

@app.route('/tickets')
def tickets():
    return render_template('tickets.html', title="Tickets")

@app.route('/about')
def about():
    return render_template('about.html', sponsors=SPONSORS, title="About the Club")

# API Endpoints
@app.route('/api/subscribe', methods=['POST'])
def api_subscribe():
    name = request.form.get('name', '').strip()
    surname = request.form.get('surname', '').strip()
    email = request.form.get('email', '').strip()
    consent = request.form.get('consent') == 'on' or request.form.get('consent') == 'true'

    if not name or not surname or not email:
        return jsonify({"success": False, "message": "All fields (Name, Surname, Email) are required."}), 400
    
    if not consent:
        return jsonify({"success": False, "message": "You must consent to data processing to subscribe."}), 400

    try:
        db = get_db()
        db.collection('newsletter_subscribers').add({
            'name': name,
            'surname': surname,
            'email': email,
            'subscribed_at': datetime.now(timezone.utc)
        })
        return jsonify({"success": True, "message": f"Thank you for subscribing, {name}!"})
    except Exception as e:
        app.logger.error(f"Error subscribing: {e}")
        return jsonify({"success": False, "message": "An error occurred while saving your subscription."}), 500

@app.route('/api/comment', methods=['POST'])
def api_comment():
    username = request.form.get('username', '').strip() or "Anonymous Fan"
    text = request.form.get('text', '').strip()

    if not text:
        return jsonify({"success": False, "message": "Comment text cannot be empty."}), 400

    try:
        db = get_db()
        db.collection('public_comments').add({
            'username': username,
            'text': text,
            'created_at': datetime.now(timezone.utc)
        })
        return jsonify({"success": True, "message": "Comment posted successfully!"})
    except Exception as e:
        app.logger.error(f"Error saving comment: {e}")
        return jsonify({"success": False, "message": "An error occurred while saving your comment."}), 500

@app.route('/api/comments', methods=['GET'])
def api_comments():
    try:
        db = get_db()
        # Retrieve comments ordered by creation date descending
        docs = db.collection('public_comments').order_by('created_at', direction='DESCENDING').stream()
        
        comments_list = []
        for doc in docs:
            data = doc.to_dict()
            # Handle ISO formatting for datetime in mock or string conversion
            created_at = data.get('created_at')
            if hasattr(created_at, 'strftime'):
                created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # Mock stores it as ISO string
                try:
                    # Parse and reformat if needed
                    dt = datetime.fromisoformat(created_at)
                    created_at_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    created_at_str = str(created_at)[:19]
                    
            comments_list.append({
                'id': doc.id,
                'username': data.get('username', 'Anonymous Fan'),
                'text': data.get('text', ''),
                'created_at': created_at_str
            })
        return jsonify({"success": True, "comments": comments_list})
    except Exception as e:
        app.logger.error(f"Error fetching comments: {e}")
        return jsonify({"success": False, "message": "An error occurred while fetching comments."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
