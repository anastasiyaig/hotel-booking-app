import pandas

df = pandas.read_csv("hotels.csv")
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")


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


print(df)  # print list of ids of hotels

hotel_id = int(input("Enter the id of the hotel: "))
hotel = Hotel(hotel_id)

if hotel.available():
    credit_card = CreditCard(card_number="1234123412341234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        hotel.book()
        name = input("Enter your name: ")
        reservation_ticket = ReservationTicket(guest_name=name, hotel_object=hotel)
        print(reservation_ticket.generate())
    else:
        print("Your payment is not successful")
else:
    print("Selected hotel is not available")
