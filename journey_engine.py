import json
from datetime import datetime, timedelta
from models import db, UserBehavior, MarketingMessage, User, Product
from sms_sender import SMSSender

sms_sender = SMSSender()

class JourneyEngine:
    def track_behavior(self, user_id, session_id, action, product_id=None, data=None):
        """
        Record user behavior in the database.
        """
        behavior = UserBehavior(
            user_id=user_id,
            session_id=session_id,
            action=action,
            product_id=product_id,
            data=data
        )
        db.session.add(behavior)
        db.session.commit()
        print(f"[JourneyEngine] Tracked behavior: {action} for session: {session_id}")

    def check_abandoned_carts(self):
        """
        Look for carts abandoned in the last 10 minutes and trigger reminders.
        """
        print("[JourneyEngine] Checking for abandoned carts...")
        abandoned_threshold = datetime.utcnow() - timedelta(minutes=10)
        # Find recent 'add_to_cart' behaviors
        recent_behaviors = UserBehavior.query.filter(
            UserBehavior.timestamp >= abandoned_threshold,
            UserBehavior.action == 'add_to_cart'
        ).all()

        for behavior in recent_behaviors:
            # Check if a purchase occurred after the add_to_cart
            existing_purchase = UserBehavior.query.filter(
                UserBehavior.session_id == behavior.session_id,
                UserBehavior.action == 'purchase',
                UserBehavior.timestamp > behavior.timestamp
            ).first()
            if not existing_purchase:
                self.send_abandoned_cart_reminder(behavior)

    def send_abandoned_cart_reminder(self, behavior):
        """
        Send a reminder SMS for an abandoned cart.
        """
        user = User.query.get(behavior.user_id) if behavior.user_id else None
        product = Product.query.get(behavior.product_id)
        if not product:
            print("[JourneyEngine] No product found for abandoned cart behavior.")
            return

        message_content = f"Don't forget your {product.name}! Complete your purchase now."

        if user and user.phone:
            # Send SMS
            sms_sender.send_sms(user.phone, message_content)
            print(f"[JourneyEngine] Sent abandoned cart reminder SMS to {user.phone}: {message_content}")

            # Record marketing message
            marketing_message = MarketingMessage(
                user_id=user.id,
                session_id=behavior.session_id,
                message_type='sms',
                content=message_content,
                status='sent'
            )
            db.session.add(marketing_message)
            db.session.commit()
        else:
            print(f"[JourneyEngine] No phone number available for session {behavior.session_id}; cannot send SMS.")
