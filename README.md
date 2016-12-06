## Online Auction System
Online auction system is an online auction house so the seller or Buyer doesn’t need to go anywhere, they can take part in the auction just sitting in the comfort of their room. 

This site also acts as an open form where buyers and sellers can come together and exchange their items. 

Every person can sell or buy any goods without meeting people personally. Selling and Delivery of goods can be done at the doorstep. Seller can get the best possible price which is greater than his target.

## Functionalities:

# Person:

He’ll be able to login, register, logout

# Seller: 

He’ll be able to sell, register and accept goods

# Buyer: 

He’ll be able to buy and see the auction details

Here buyer and seller are sub classes of person.

# Seller

•	Seller can upload auction product.
•	Seller can set the starting prize of the item.
•	Seller can view the bid information for their items. 
•	Seller can bid for product.

# Buyer

•	Buyer can buy package for auction.
•	Buyer can view detail of product.
•	Buyer can bid on particular product.
•	Buyer can also modify the bidding prize.

# Models:

1. Person   {person_id, first_name, last_name, address, contact, password} 
2. Seller   {selling_details}
3. Buyer   {purchase_details}
4. Goods   {good_id, good_name, category, seller_id} 
5. Sold Goods  {purchaser_id, target_price, sold_price, date} 
6. Progress Goods  {purchaser_id, auction_rate, auction_date}
