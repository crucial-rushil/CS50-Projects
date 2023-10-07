-- Keep a log of any SQL queries you execute as you solve the mystery.

--GIVEN: theft took place on July 28, 2020 and that it took place on Chamberlin Street

--Find out tables in data base
.tables

--Find out schema of crime scene table
.schema crime_scene_reports

--Find out the description
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = "Chamberlin Street";
--OBTAINED Description: Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
--Interviews were conducted today with three witnesses who were present at the time
--each of their interview transcripts mentions the courthouse.

--Find out schema of Interview table
.schema interviews

--Find out the witness testimony and their names
SELECT name,transcript FROM interviews WHERE transcript LIKE "%courthouse%";

--Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
--Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
--Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

--Find out the possible cars
SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <=25 AND activity = "exit";
--Results:
--5P2BI95 | exit
--94KL13X | exit
--6P58WS2 | exit
--4328GD8 | exit
--G412CB7 | exit
--L93JTIZ | exit
--322W7JE | exit
--0NTHK55 | exit

--FIND out the names of People Who withdrew money as per Eugene's Description
SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND day = 28 AND month = 7 AND atm_location = "Fifer Street" and transaction_type = "withdraw"));

--Suspect List:
--Bobby
--Elizabeth
--Victoria
--Madison
--Roy
--Danielle
--Russell
--Ernest

--FIND out the Phone numbers per Raymonds caller description
SELECT caller FROM phone_calls WHERE year = 2020 AND day = 28 AND month = 7 AND duration < 60;
--(130) 555-0289
--(499) 555-9472
--(367) 555-5533
--(499) 555-9472
--(286) 555-6063
--(770) 555-1861
--(031) 555-6622
--(826) 555-1652
--(338) 555-6650

--Earliest Flight the thief from fiftyville boarded and where they are headed to
SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE year = 2020 AND day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour,minute LIMIT 1);
--Thief Headed to London,England


--Obtain the theif's passport number/seat
SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2020 AND day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour,minute LIMIT 1);
--7214083635
--1695452385
--5773159633
--1540955065
--8294398571
--1988161715
--9878712108
--8496433585


--Cross compare the data to find the thief (use SELECT queries from earlier and combine)
SELECT name FROM people
WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 AND day = 28 AND month = 7 AND duration < 60)
AND name IN (SELECT name FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE year = 2020 AND day = 28 AND month = 7 AND atm_location = "Fifer Street" and transaction_type = "withdraw")))
AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE year = 2020 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <=25 AND activity = "exit")
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE year = 2020 AND day = 29 AND month = 7 AND origin_airport_id = (SELECT id FROM airports WHERE city = "Fiftyville") ORDER BY hour,minute LIMIT 1));
--Thief: Ernest

--Find the thief's accomplice's phone number
SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = "Ernest") AND year = 2020 AND day = 28 AND month = 7 AND duration < 60;
--Accomplice's Phone number: (375) 555-8161

--Find the accomplice (use their phone_number)
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE name = "Ernest") AND year = 2020 AND day = 28 AND month = 7 AND duration < 60);
--Accomplice: Berthold