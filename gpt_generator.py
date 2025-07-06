import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GPTGenerator:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        
        if self.openai_key:
            openai.api_key = self.openai_key
        
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
    
    def generate_response(self, message, context="customer_support"):
        """Generate a response using available AI service"""
        try:
            if self.openai_key:
                return self._generate_with_openai(message, context)
            elif self.gemini_key:
                return self._generate_with_gemini(message, context)
            else:
                return self._generate_fallback_response(message, context)
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._generate_fallback_response(message, context)
    
    def _generate_with_openai(self, message, context):
        """Generate response using OpenAI GPT"""
        system_prompt = self._get_system_prompt(context)
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_with_gemini(self, message, context):
        """Generate response using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        system_prompt = self._get_system_prompt(context)
        
        prompt = f"{system_prompt}\n\nUser: {message}\nAssistant:"
        response = model.generate_content(prompt)
        
        return response.text.strip()
    
    def _generate_fallback_response(self, message, context):
        """Generate fallback response when no AI service is available"""
        fallback_responses = {
            "customer_support": [
                "Thank you for your message! I'm here to help you with any questions about our products.",
                "I'd be happy to assist you! What specific product information are you looking for?",
                "Thanks for reaching out! How can I help you find the perfect product today?",
                "I'm here to help! What questions do you have about our products or services?",
                "Great question! Let me help you with that. What specific information do you need?"
            ],
            "abandoned_cart": [
                "Don't forget about your cart! Complete your purchase and enjoy our amazing products.",
                "Your cart is waiting! Come back and complete your order to get these great items.",
                "Still thinking about your purchase? Your cart items are reserved for you!",
                "Your cart has some great items! Complete your purchase before they're gone.",
                "Ready to complete your order? Your cart is waiting for you!"
            ],
            "product_interest": [
                "Great choice! This product has excellent reviews from our customers.",
                "This is one of our most popular items! Would you like to know more about it?",
                "Excellent selection! This product offers great value and quality.",
                "This product is a customer favorite! Perfect choice for your needs.",
                "Great find! This product has been highly rated by our customers."
            ]
        }
        
        responses = fallback_responses.get(context, fallback_responses["customer_support"])
        return responses[hash(message) % len(responses)]
    
    def _get_system_prompt(self, context):
        """Get system prompt based on context"""
        prompts = {
            "customer_support": "You are a helpful customer support assistant for an e-commerce store. Be friendly, professional, and helpful in answering customer questions about products, orders, and services. Keep responses concise and actionable.",
            "abandoned_cart": "You are a marketing assistant helping recover abandoned carts. Create persuasive but not pushy messages to encourage customers to complete their purchases. Focus on value, urgency, and customer benefits.",
            "product_interest": "You are a product recommendation assistant. Help customers learn about products they're interested in. Highlight key features, benefits, and value propositions. Be enthusiastic but honest.",
            "purchase_confirmation": "You are a customer success assistant confirming purchases. Be warm, appreciative, and provide helpful next steps. Express gratitude and build customer loyalty."
        }
        
        return prompts.get(context, prompts["customer_support"])
    
    def generate_abandoned_cart_message(self, username, product_name):
        """Generate personalized abandoned cart message"""
        message = f"Hey {username}, you left {product_name} in your cart! Don't miss out on this great product. Complete your purchase now and get it delivered to you soon!"
        return self.generate_response(message, "abandoned_cart")
    
    def generate_product_interest_message(self, product_name):
        """Generate message for product interest"""
        message = f"I see you're interested in {product_name}. This is a great choice!"
        return self.generate_response(message, "product_interest")
    
    def generate_purchase_confirmation(self, username):
        """Generate purchase confirmation message"""
        message = f"Thank you {username} for your purchase! We're processing your order and will send you updates soon."
        return self.generate_response(message, "purchase_confirmation")
    
    def generate_personalized_recommendation(self, username, viewed_products, recommended_products):
        """Generate personalized product recommendation"""
        message = f"Based on your interest in {', '.join(viewed_products)}, you might like these products: {', '.join(recommended_products)}"
        return self.generate_response(message, "product_interest") 