ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_sign_and_degree(abs_deg):
    sign = int(abs_deg // 30)  # 0–11
    deg = abs_deg % 30
    return sign, deg

def get_absolute_degree(sign_index, degree_in_sign):
    return sign_index * 30 + degree_in_sign

def get_sign_and_degree(absolute_deg):
    sign = int(absolute_deg // 30)
    degree_in_sign = absolute_deg % 30
    return sign, degree_in_sign

# def rotate_chart(mapping, asc_sign_index):
#     rotated = {i: {'planets': [], 'zodiac': ''} for i in range(1, 13)}
#     asc_house = mapping.get("Ascendant")
#     for body, house in mapping.items():
#         shift = (house - asc_house) % 12
#         new_house = shift + 1
#         rotated[new_house]['planets'].append(body)
#     for i in range(1, 13):
#         zodiac_index = (asc_sign_index + i - 1) % 12
#         rotated[i]['zodiac'] = ZODIAC_SIGNS[zodiac_index] + f" ({zodiac_index + 1})"
#     return rotated



def rotate_chart(mapping, asc_sign_index):
    # Create rotated structure
    rotated = {i: {'planets': [], 'zodiac': ''} for i in range(1, 13)}

    # Determine original sign index of each house
    sign_to_house = {((asc_sign_index + i) % 12) + 1: i + 1 for i in range(12)}

    # Step 1: Move all planets to correct rotated houses
    for body, house in mapping.items():
        if body == "Ascendant":
            continue
        shift = (house - mapping["Ascendant"]) % 12
        new_house = shift + 1
        rotated[new_house]['planets'].append(body)

    # Step 2: Label rotated zodiac signs
    for i in range(1, 13):
        zodiac_index = (asc_sign_index + i - 1) % 12
        rotated[i]['zodiac'] = ZODIAC_SIGNS[zodiac_index] + f" ({zodiac_index + 1})"

    return rotated





def get_d1_chart(planets_raw, asc_deg):
    asc_sign_index = int(asc_deg // 30)  # 0 for Aries, 1 for Taurus, ..., 11 for Pisces
    chart = {}
    for planet, abs_deg in planets_raw.items():
        planet_sign_index = int(abs_deg // 30)
        house = ((planet_sign_index - asc_sign_index) % 12) + 1
        chart[planet] = house
    chart['Ascendant'] = 1  # Always 1st house
    return rotate_chart(chart, asc_sign_index)

def generic_chart(planets_raw, asc_deg, transform_fn):
    chart = {}
    for planet, abs_deg in planets_raw.items():
        chart[planet] = transform_fn(abs_deg)
    chart['Ascendant'] = transform_fn(asc_deg)
    asc_sign_index = int(asc_deg // 30)
    return rotate_chart(chart, asc_sign_index)

# def get_d3_chart(planets_raw, asc_deg):
#     def transform(abs_deg):
#         sign, deg = get_sign_and_degree(abs_deg)
#         drekkana = int(deg // 10)
#         return (sign if drekkana == 0 else (sign + 5 if drekkana == 1 else (sign + 9))) % 12 + 1
#     return generic_chart(planets_raw, asc_deg, transform)





# def get_d3_chart(planets_raw, asc_deg):
#     def transform(abs_deg):
#         sign, deg = get_sign_and_degree(abs_deg)  # sign = 0 for Aries, ..., 11 for Pisces
#         drekkana = int(deg // 10)

#         if drekkana == 0:
#             new_sign = sign
#         elif drekkana == 1:
#             new_sign = (sign + 5) % 12
#         else:  # drekkana == 2
#             new_sign = (sign + 9) % 12

#         return new_sign + 1  # +1 to make it 1-based (1 = Aries, ..., 12 = Pisces)

#     return generic_chart(planets_raw, asc_deg, transform)



# def get_d3_chart(planets_raw, asc_deg):
#     def transform(abs_deg):
#         sign, deg = get_sign_and_degree(abs_deg)
#         drekkana = int(deg // 10)

#         if drekkana == 0:
#             new_sign = sign
#         elif drekkana == 1:
#             new_sign = (sign + 5) % 12
#         else:  # drekkana == 2
#             new_sign = (sign + 9) % 12

#         return new_sign

#     chart = {}
#     for planet, abs_deg in planets_raw.items():
#         chart[planet] = transform(abs_deg)

#     asc_sign_index = transform(asc_deg)  # rotated ascendant's sign index
#     asc_house = 1  # always placed in 1st house

#     rotated = {i: {'planets': [], 'zodiac': ''} for i in range(1, 13)}
#     for body, sign_index in chart.items():
#         house = ((sign_index - asc_sign_index) % 12) + 1
#         rotated[house]['planets'].append(body)

#     for i in range(1, 13):
#         zodiac_index = (asc_sign_index + i - 1) % 12
#         rotated[i]['zodiac'] = ZODIAC_SIGNS[zodiac_index] + f" ({zodiac_index + 1})"

#     return rotated





def get_d3_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        drekkana = int(deg // 10)

        if drekkana == 0:
            new_sign = sign
        elif drekkana == 1:
            new_sign = (sign + 5) % 12
        else:  # drekkana == 2
            new_sign = (sign + 9) % 12

        return new_sign  # returns 0–11

    transformed_planets = {}
    for planet, abs_deg in planets_raw.items():
        transformed_planets[planet] = transform(abs_deg)

    asc_sign_index = transform(asc_deg)  # 0–11
    mapping = {}

    # Now convert transformed sign indices into house numbers based on ascendant
    for planet, sign_index in transformed_planets.items():
        house = ((sign_index - asc_sign_index) % 12) +1
        mapping[planet] = house

    mapping["Ascendant"] = 1  # always put asc in 1st house
    return rotate_chart(mapping, asc_sign_index)




def get_d6_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        is_odd = (sign % 2 == 0)
        shashtiamsa = int(deg * 2)
        return ((sign + shashtiamsa) if is_odd else (sign + (59 - shashtiamsa))) % 12 + 1
    return generic_chart(planets_raw, asc_deg, transform)

def get_d9_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        navamsa_index = int(deg * 3)
        return ((sign + navamsa_index) if sign % 2 == 0 else (sign + (8 - navamsa_index))) % 12 + 1
    return generic_chart(planets_raw, asc_deg, transform)

def get_d30_chart(planets_raw, asc_deg):
    def trimsamsa_calc(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        if sign % 2 == 0:
            return [6, 10, 8, 1, 11][[deg <= 5, deg <= 10, deg <= 18, deg <= 25, True].index(True)]
        else:
            return [11, 1, 8, 10, 6][[deg <= 5, deg <= 12, deg <= 20, deg <= 25, True].index(True)]
    return generic_chart(planets_raw, asc_deg, trimsamsa_calc)

def get_d60_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        return int(abs_deg * 2) % 12 + 1
    return generic_chart(planets_raw, asc_deg, transform)
