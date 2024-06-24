def get_user_info():
    user_info = {}
    user_info['age'] = int(input("나이를 입력하세요: "))
    user_info['location'] = input("현재 사시는 거주지를 간단하게 입력하세요 (서울/경기/인천 등): ").strip()
    user_info['destination'] = input("주로 이동하는 지역을 입력하세요 (서울 내/서울 외): ").strip()
    user_info['daily_transport_rides'] = int(input("하루 대중교통 이용 횟수를 입력하세요: "))
    user_info['discount_category'] = input("할인 대상 여부를 입력하세요 (청년/저소득층/없음): ").strip()
    user_info['days_per_month'] = int(input("한 달에 며칠 대중교통을 이용하나요?: "))
    return user_info

def calculate_monthly_spending(daily_rides, days_per_month):
    subway_ride_cost = 1400
    bus_ride_cost = 1500
    # Assuming half of the rides are by subway and half by bus
    daily_cost = (subway_ride_cost + bus_ride_cost) / 2 * daily_rides
    monthly_spending = daily_cost * days_per_month
    return monthly_spending

def calculate_k_pass_benefit(user_info, monthly_spending):
    if user_info['daily_transport_rides'] * user_info['days_per_month'] < 15:
        return 0

    if user_info['discount_category'] == '청년':
        discount_rate = 0.30
    elif user_info['discount_category'] == '저소득층':
        discount_rate = 0.53
    else:
        discount_rate = 0.20

    max_discount_spending = min(monthly_spending, 60 * 2500)
    discount = max_discount_spending * discount_rate
    return discount

def calculate_climate_card_benefit(monthly_spending):
    if monthly_spending < 62000:
        return 0
    return monthly_spending - 62000

def calculate_region_pass_benefit(user_info, monthly_spending):
    if user_info['location'] == '경기' or user_info['location'] == '인천':
        if user_info['discount_category'] == '청년' and user_info['age'] <= 39:
            return monthly_spending * 0.20
        elif user_info['age'] < 19 or user_info['age'] > 65:
            return monthly_spending * 0.30
        else:
            return monthly_spending * 0.20
    return 0

def compare_cards(user_info):
    monthly_spending = calculate_monthly_spending(user_info['daily_transport_rides'], user_info['days_per_month'])
    
    if user_info['destination'] == '서울 외':
        best_card = "K-PASS 카드"
        best_benefit = calculate_k_pass_benefit(user_info, monthly_spending)
    else:
        k_pass_benefit = calculate_k_pass_benefit(user_info, monthly_spending)
        climate_card_benefit = calculate_climate_card_benefit(monthly_spending)
        region_pass_benefit = calculate_region_pass_benefit(user_info, monthly_spending)

        if k_pass_benefit > climate_card_benefit and k_pass_benefit > region_pass_benefit:
            best_card = "K-PASS 카드"
            best_benefit = k_pass_benefit
        elif climate_card_benefit > k_pass_benefit and climate_card_benefit > region_pass_benefit:
            best_card = "기후동행카드"
            best_benefit = climate_card_benefit
        else:
            best_card = "지역 패스 (The 경기패스 또는 인천 I-패스)"
            best_benefit = region_pass_benefit

    return best_card, best_benefit

# 메인 함수
if __name__ == "__main__":
    user_info = get_user_info()
    best_card, best_benefit = compare_cards(user_info)
    print(f"사용자에게 가장 유리한 카드는 {best_card}이며, 예상 혜택은 {best_benefit}원입니다.")
    input("결과를 확인했으면 엔터를 눌러 종료하세요.")
