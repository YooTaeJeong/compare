# app.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h1>대중교통 카드 비교</h1>
        <form action="/compare" method="post">
            나이를 입력하세요: <input type="text" name="age"><br>
            현재 사시는 거주지를 간단하게 입력하세요: <input type="text" name="location"><br>
            주로 이동하는 지역을 입력하세요 (서울 내/서울 외): <input type="text" name="destination"><br>
            하루 평균 대중교통 이용 횟수를 입력하세요: <input type="text" name="daily_transport_rides"><br>
            할인 대상 여부를 입력하세요 (청년/저소득층/없음): <input type="text" name="discount_category"><br>
            <input type="submit" value="비교하기">
        </form>
    '''

@app.route('/compare', methods=['POST'])
def compare():
    user_info = {
        'age': int(request.form['age']),
        'location': request.form['location'],
        'destination': request.form['destination'],
        'daily_transport_rides': int(request.form['daily_transport_rides']),
        'discount_category': request.form['discount_category']
    }

    monthly_transport_rides = user_info['daily_transport_rides'] * 30
    monthly_transport_spending = user_info['daily_transport_rides'] * 30 * 1400  # 지하철 기본요금으로 계산

    def calculate_k_pass_benefit(user_info, monthly_transport_spending):
        if user_info['daily_transport_rides'] < 15:
            return 0

        if user_info['discount_category'] == '청년':
            discount_rate = 0.30
        elif user_info['discount_category'] == '저소득층':
            discount_rate = 0.53
        else:
            discount_rate = 0.20

        max_discount_spending = min(monthly_transport_spending, 60 * 1500)
        discount = max_discount_spending * discount_rate
        return discount

    def calculate_climate_card_benefit(monthly_transport_spending):
        if monthly_transport_spending < 62000:
            return 0

        return monthly_transport_spending - 62000

    if user_info['destination'] == '서울 외':
        best_card = "K-PASS 카드"
        best_benefit = calculate_k_pass_benefit(user_info, monthly_transport_spending)
    else:
        k_pass_benefit = calculate_k_pass_benefit(user_info, monthly_transport_spending)
        climate_card_benefit = calculate_climate_card_benefit(monthly_transport_spending)

        if k_pass_benefit > climate_card_benefit:
            best_card = "K-PASS 카드"
            best_benefit = k_pass_benefit
        else:
            best_card = "기후동행카드"
            best_benefit = climate_card_benefit

    return f"사용자에게 가장 유리한 카드는 {best_card}이며, 예상 혜택은 {best_benefit}원입니다."

if __name__ == '__main__':
    app.run(debug=True)
