# app/utils/email.py
import requests
from flask import current_app
from jinja2 import Template

class EmailService:
    @staticmethod
    def _get_order_template_html(order, lang='ja'):
        if lang == 'ja':
            template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body { font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { text-align: center; padding: 20px; background-color: #4F46E5; color: white; }
                    .content { padding: 20px; background-color: #ffffff; }
                    .order-details { margin: 20px 0; }
                    .total { font-size: 1.2em; font-weight: bold; }
                    .footer { text-align: center; padding: 20px; color: #666; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>ご注文ありがとうございます</h1>
                    </div>
                    
                    <div class="content">
                        <h2>注文詳細</h2>
                        <p>注文番号: {{ order.id }}</p>
                        
                        <div class="order-details">
                            {% for item in order.order_items %}
                            <div style="margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
                                <p>デザインID: {{ item.design_id }}</p>
                                <p>サイズ: {{ item.size }}</p>
                                <p>カラー: {{ item.color }}</p>
                                <p>数量: {{ item.quantity }}</p>
                                <p>価格: ¥{{ "{:,}".format(item.price) }}</p>
                            </div>
                            {% endfor %}
                            
                            <p class="total">
                                合計金額: ¥{{ "{:,}".format(order.total_amount) }}
                            </p>
                        </div>
                        
                        <div style="margin-top: 20px;">
                            <h3>配送先情報</h3>
                            <p>{{ order.shipping_address.name }}</p>
                            <p>{{ order.shipping_address.address }}</p>
                            <p>{{ order.shipping_address.city }}</p>
                            <p>{{ order.shipping_address.postal_code }}</p>
                            <p>{{ order.shipping_address.country }}</p>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>ご不明な点がございましたら、お気軽にお問い合わせください。</p>
                        <p>© 2024 CustomAI Tee. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        else:
            template = """[English template here]"""
            
        return Template(template)

    @staticmethod
    def send_order_confirmation(order, recipient_email, lang='ja'):
        try:
            mailgun_domain = current_app.config['MAILGUN_DOMAIN']
            mailgun_api_key = current_app.config['MAILGUN_API_KEY']
            
            print(f"Preparing to send email to: {recipient_email}")
            print(f"Using Mailgun domain: {mailgun_domain}")

            template = EmailService._get_order_template_html(order, lang)
            html_content = template.render(order=order)
            
            print("Template rendered successfully")

            # Mailgun API URLの構築
            mailgun_url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"
            print(f"Mailgun API URL: {mailgun_url}")

            # メールデータの準備
            email_data = {
                "from": f"CustomAI Tee <noreply@{mailgun_domain}>",
                "to": recipient_email,
                "subject": "ご注文ありがとうございます - CustomAI Tee" if lang == 'ja' else "Thank you for your order - CustomAI Tee",
                "html": html_content
            }
            
            if current_app.config.get('ADMIN_EMAIL'):
                email_data["cc"] = current_app.config['ADMIN_EMAIL']

            print("Sending request to Mailgun...")
            response = requests.post(
                mailgun_url,
                auth=("api", mailgun_api_key),
                data=email_data
            )
            
            print(f"Mailgun response status: {response.status_code}")
            print(f"Mailgun response content: {response.text}")

            if response.status_code == 200:
                print(f"Email sent successfully to {recipient_email}")
                return True
            else:
                print(f"Failed to send email. Status code: {response.status_code}")
                print(f"Error response: {response.text}")
                return False

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    @staticmethod
    def send_shipping_notification(order, recipient_email, tracking_number=None, lang='ja'):
        try:
            mailgun_domain = current_app.config['MAILGUN_DOMAIN']
            mailgun_api_key = current_app.config['MAILGUN_API_KEY']

            subject = '商品発送のお知らせ - CustomAI Tee' if lang == 'ja' else 'Your order has been shipped - CustomAI Tee'
            
            template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body { font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>商品を発送いたしました</h1>
                    <p>注文番号: {{ order.id }}</p>
                    {% if tracking_number %}
                    <p>追跡番号: {{ tracking_number }}</p>
                    {% endif %}
                </div>
            </body>
            </html>
            """
            
            html_content = Template(template).render(
                order=order,
                tracking_number=tracking_number
            )

            response = requests.post(
                f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
                auth=("api", mailgun_api_key),
                data={
                    "from": f"CustomAI Tee <noreply@{mailgun_domain}>",
                    "to": recipient_email,
                    "subject": subject,
                    "html": html_content
                }
            )

            return response.status_code == 200

        except Exception as e:
            print(f"Error sending shipping notification: {str(e)}")
            return False