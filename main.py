import pandas

df = pandas.read_csv("hotels.csv")
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.hotel_name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self) -> bool:
        """Checks if the hotel is available"""
        if df.loc[df["id"] == self.hotel_id, "available"].squeeze() == "yes":
            return True

    def book(self):
        """Book a hotel by changing the availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass

    def available(self) -> bool:
        pass


class ReservationTicket:
    def __init__(self, guest_name, hotel_object):
        self.guest_name = guest_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for reservation, which is now confirmed.
        Name: {self.guest_name}
        Hotel name: {self.hotel.hotel_name}
        """
        return content


class SpaReservationTicket:
    def __init__(self, guest_name, hotel_object):
        self.guest_name = guest_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for SPA reservation.
        Name: {self.guest_name}
        Hotel name: {self.hotel.hotel_name}
        """
        return content


class CreditCard:
    def __init__(self, card_number):
        self.number = card_number

    def validate(self, expiration, holder, cvc):
        card_data = {
            "number": self.number,
            "expiration": expiration,
            "holder": holder,
            "cvc": cvc
        }
        if card_data in df_cards:
            return True


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True


print(df)  # print list of ids of hotels

hotel_id = int(input("Enter the id of the hotel: "))
spa_hotel = SpaHotel(hotel_id)

if spa_hotel.available():
    credit_card = SecureCreditCard(card_number="1234123412341234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            spa_hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(guest_name=name, hotel_object=spa_hotel)
            print(reservation_ticket.generate())
            spa_choice = input("Do you want to add spa to your booking?")
            match spa_choice.lower():
                case "yes":
                    if spa_hotel.available():
                        spa_ticket = SpaReservationTicket(guest_name=name, hotel_object=spa_hotel)
                        print(spa_ticket.generate())
                    else:
                        print("Sorry, we don't have any free slots now")
                case "no":
                    print("You can book spa any day of your stay on demand, please check the availability at the "
                          "service desk")
        else:
            print("Your card authentication is not successful")
    else:
        print("Your payment is not successful")
else:
    print("Selected hotel is not available")
