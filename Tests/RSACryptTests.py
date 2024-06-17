import string
import unittest

from Crypts.RSACrypt import RSACrypt


class RSACryptTests(unittest.TestCase):
    def test_ordinal(self):
        crypt = RSACrypt()
        text = 'Pepa je strašně hodný hoch a je mu -1 let. :-)'
        public, private = crypt.create_keys()

        enc = crypt.encrypt(text, public)
        decrypted_text = crypt.decrypt(enc, private)
        self.assertEqual(decrypted_text, text)

    def test_all_chars(self):
        crypt = RSACrypt()
        text = '!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýýþÿ'
        public, private = crypt.create_keys()

        enc = crypt.encrypt(text, public)
        decrypted_text = crypt.decrypt(enc, private)
        self.assertEqual(decrypted_text, text)

    def test_all_chars_ordinal_usage(self):
        crypt = RSACrypt()
        text = ';+ěščřžýáíé=qwertzuiopú)asdfghjklABCDEFGHIJKLMNOPQRSTUVWXYů§¨yxcvbnm,.-|°1234567890%ˇ(/\'!"_:?~ˇ^˘°˛`˙´˝¨¨¸×÷¤ß$*><'
        public, private = crypt.create_keys()

        enc = crypt.encrypt(text, public)
        decrypted_text = crypt.decrypt(enc, private)
        self.assertEqual(decrypted_text, text)

    def test_short_text(self):
        crypt = RSACrypt()
        text = 'P'
        public, private = crypt.create_keys()

        enc = crypt.encrypt(text, public)
        decrypted_text = crypt.decrypt(enc, private)
        self.assertEqual(decrypted_text, text)

    def test_long_text(self):
        crypt = RSACrypt()
        text = 'jen mám trochu pocit, že se mi chce na záchod a do koupelny, už má vytvořeny jednoduché a podle předpovědi počasí pod psa, ale celá věc za nesmírně důležité, aby se to neopakovalo a po zapracování připomínek k návrhu na prodej automobilů značky husarský kousek, když vás to tak použijeme v takové podobě, jak ji známe dnes, má na to ještě v době, kdy jsme všichni byli v pohodě, ale jak jsem si to vynahradila a pokud by se mu na ní líbilo a všechno se obrátit přímo na pobočce v brně mi vysvětlil, že je to stará fasáda, nová verze známého střediska pro koně, jednou rukou místo obvyklého pobytu nebo sídla a připravovala se na ni podívala a pak přes celé město, nebo je to jenom pro představu, co všechno musí udělat obrázek o tom, jak to vlastně všechno začalo?'
        public, private = crypt.create_keys()

        enc = crypt.encrypt(text, public)
        decrypted_text = crypt.decrypt(enc, private)
        self.assertEqual(decrypted_text, text)

    def test_invert_keys(self):
        crypt = RSACrypt()
        text = string.digits + string.ascii_letters
        public, private = crypt.create_keys()

        enc = crypt.encrypt(text, private)
        decrypted_text = crypt.decrypt(enc, public)
        self.assertEqual(decrypted_text, text)

    def test_out_of_range_chars(self):
        crypt = RSACrypt()
        text = '丁Ж'
        public, private = crypt.create_keys()

        self.assertRaises(OverflowError, crypt.encrypt, text, public)
