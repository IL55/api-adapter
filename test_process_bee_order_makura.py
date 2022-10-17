from unittest.mock import MagicMock, patch
import unittest

from process_bee_order_makura import get_phone, process_order_for_makura


raw_order = {
    "ErrorMessage": "None",
    "ErrorCode": 0,
    "ErrorDescription": "NoError",
    "Data": {
        "RebateDifference": 0.0,
        "ShippingIds": [

        ],
        "AcceptLossOfReturnRight": False,
        "Id": "None",
        "OrderNumber": "None",
        "State": 6,
        "VatMode": 0,
        "CreatedAt": "2021-11-01T00:00:00",
        "ShippedAt": "None",
        "ConfirmedAt": "None",
        "PayedAt": "None",
        "SellerComment": "None",
        "Comments": [

        ],
        "InvoiceNumberPrefix": "None",
        "InvoiceNumberPostfix": "None",
        "InvoiceNumber": "None",
        "InvoiceDate": "None",
        "InvoiceAddress": {
            "BillbeeId": 635436463,
            "FirstName": "test",
            "LastName": "test",
            "Company": "test",
            "NameAddition": "test",
            "Street": "test",
            "HouseNumber": "25",
            "Zip": "12345",
            "City": "test",
            "CountryISO2": "DE",
            "Country": "DE",
            "Line2": "te",
            "Email": "test_test@seznam.cz",
            "State": "None",
            "Phone": "00420111111111"
        },
        "ShippingAddress": {
            "BillbeeId": 635436463,
            "FirstName": "test1",
            "LastName": "test2",
            "Company": "test3",
            "NameAddition": "test",
            "Street": "test4",
            "HouseNumber": "25",
            "Zip": "12345",
            "City": "test",
            "CountryISO2": "DE",
            "Country": "DE",
            "Line2": "te",
            "Email": "test_test@seznam.cz",
            "State": "None",
            "Phone": "00420111111111"
        },
        "PaymentMethod": 22,
        "ShippingCost": 0.0,
        "TotalCost": 19.9,
        "AdjustmentCost": 0.0,
        "AdjustmentReason": "None",
        "OrderItems": [
            {
                "BillbeeId": 545435345,
                "TransactionId": "None",
                "Product": {
                    "OldId": "None",
                    "Id": "None",
                    "Title": "Title",
                    "Weight": "None",
                    "SKU": "BK-302017N",
                    "SkuOrId": "BK-302017N",
                    "IsDigital": False,
                    "Images": "None",
                    "EAN": "8595650901132",
                    "PlatformData": "None",
                    "TARICCode": "1632-15770s",
                    "CountryOfOrigin": "None",
                    "BillbeeId": 6011843543565
                },
                "Quantity": 1.0,
                "TotalPrice": 19.9,
                "TaxAmount": 3.453719008264463,
                "TaxIndex": 1,
                "Discount": 0.0,
                "Attributes": [

                ],
                "GetPriceFromArticleIfAny": False,
                "IsCoupon": False,
                "ShippingProfileId":"None",
                "DontAdjustStock": False,
                "UnrebatedTotalPrice":19.9,
                "SerialNumber":"None",
                "InvoiceSKU":"BK-302017N"
            }
        ],
        "Currency": "EUR",
        "Seller": {
            "Platform": "None",
            "BillbeeShopName": "None",
            "BillbeeShopId": "None",
            "Id": "7543c8df-3cdf-4c8e-b22a-06fb6fc5df83",
            "Nick": "None",
            "FirstName": "None",
            "LastName": "None",
            "FullName": "",
            "Email": "None"
        },
        "Buyer": "None",
        "UpdatedAt": "None",
        "TaxRate1": 21.0,
        "TaxRate2": 15.0,
        "BillBeeOrderId": 170081072,
        "BillBeeParentOrderId": "None",
        "VatId": "None",
        "Tags": [
            "66"
        ],
        "ShipWeightKg": "None",
        "LanguageCode": "None",
        "PaidAmount": 0.0,
        "ShippingProfileId": "None",
        "ShippingProviderId": "None",
        "ShippingProviderProductId": "None",
        "ShippingProviderName": "None",
        "ShippingProviderProductName": "None",
        "ShippingProfileName": "None",
        "PaymentInstruction": "None",
        "IsCancelationFor": "None",
        "PaymentTransactionId": "None",
        "DistributionCenter": "None",
        "DeliverySourceCountryCode": "None",
        "CustomInvoiceNote": "None",
        "CustomerNumber": "1200251",
        "PaymentReference": "None",
        "ShippingServices": "None",
        "Customer": {
            "Id": 57917122,
            "Name": "test",
            "Email": "test_test@seznam.cz",
            "Tel1": "00420111111111",
            "Tel2": "None",
            "Number": 1200251,
            "PriceGroupId": "None",
            "LanguageId": "None",
            "DefaultMailAddress": {
                "Id": 31056164,
                "TypeId": 1,
                "TypeName": "EMail",
                "SubType": "default",
                "Value": "test_test@seznam.cz"
            },
            "DefaultCommercialMailAddress": "None",
            "DefaultStatusUpdatesMailAddress": "None",
            "DefaultPhone1": {
                "Id": 31056165,
                "TypeId": 2,
                "TypeName": "Phone",
                "SubType": "phone",
                "Value": "00420111111111"
            },
            "DefaultPhone2": "None",
            "DefaultFax": "None",
            "VatId": "None",
            "Type": 0,
            "MetaData": [
                {
                    "Id": 31056164,
                    "TypeId": 1,
                    "TypeName": "EMail",
                    "SubType": "default",
                    "Value": "test_test@seznam.cz"
                },
                {
                    "Id": 31056165,
                    "TypeId": 2,
                    "TypeName": "Phone",
                    "SubType": "phone",
                    "Value": "00420111111111"
                }
            ],
            "ArchivedAt": "None",
            "RestoredAt": "None"
        },
        "History": [],
        "Payments": [],
        "LastModifiedAt": "2021-11-01T20:33:27.017",
        "ArchivedAt": "None",
        "RestoredAt": "None",
        "ApiAccountId": "None",
        "ApiAccountName": "None",
        "MerchantVatId": "None",
        "CustomerVatId": "None",
        "IsFromBillbeeApi": False
    }
}


products = [
    {
        "fulfillmentProductCode": "A01-002",
        "quantity": 1
    },
    {
        "fulfillmentProductCode": "A01-004",
        "quantity": 3
    }
]

makura_order = {
    "external_id": "1632-170081072",
    "carrier_id": 43,
    "payment_id": 2,
    "note": "",
    "delivery_address": {
        "firstname": "test1",
        "lastname": "test2",
        "company": "test3",
        "street": "test4 25",
        "zip": "12345",
        "city": "test",
        "country": "DE",
        "email": "test_test@seznam.cz",
        "phone": "00420111111111"
    },
    "products": [
        {
            "catalog_number": "A01-002",
            "quantity": 1
        },
        {
            "catalog_number": "A01-004",
            "quantity": 3
        }
    ]
}

class Makura_process_order(unittest.TestCase):
    def test_process_order_for_makura_none(self):
        result = process_order_for_makura("170081072", {})
        self.assertEqual(result, None)

    @patch("process_bee_order_makura.get_bee_products", MagicMock(return_value=products))
    def test_process_order_for_makura_ok(self):
        result = process_order_for_makura("170081072", raw_order)
        self.assertDictEqual(result, makura_order)


class MakuraTestPhone(unittest.TestCase):
    def test_phones(self):
        self.assertEqual(
            get_phone("+420123123123"),
            "+420123123123"
        )

        self.assertEqual(
            get_phone("420/123123123"),
            "420123123123"
        )

        self.assertEqual(
            get_phone(""),
            "+49111111111"
        )

        self.assertEqual(
            get_phone("420+123+123+123"),
            "420123123123"
        )



