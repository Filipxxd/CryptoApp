import string
import unittest

from core.crypts.RSACrypt import RSACrypt


class RSACipherTests(unittest.TestCase):
    def test_ordinal(self):
        crypt = RSACrypt()
        text = 'Pepa je strašně hodný hoch a je mu -1 let. :-)'
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        enc = crypt.encrypt(text, public)
        dec = crypt.decrypt(enc, private)
        self.assertTrue(dec == text)

    def test_all_chars(self):
        crypt = RSACrypt()
        text = '!\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýýþÿ'
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        enc = crypt.encrypt(text, public)
        dec = crypt.decrypt(enc, private)
        self.assertTrue(dec == text)

    def test_all_chars_ordinal_usage(self):
        crypt = RSACrypt()
        text = ';+ěščřžýáíé=qwertzuiopú)asdfghjklABCDEFGHIJKLMNOPQRSTUVWXYů§¨yxcvbnm,.-|°1234567890%ˇ(/\'!"_:?~ˇ^˘°˛`˙´˝¨¨¸×÷¤ß$*><'
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        enc = crypt.encrypt(text, public)
        dec = crypt.decrypt(enc, private)
        self.assertTrue(dec == text)

    def test_short_text(self):
        crypt = RSACrypt()
        text = 'P'
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        enc = crypt.encrypt(text, public)
        dec = crypt.decrypt(enc, private)
        self.assertTrue(dec == text)

    def test_long_text(self):
        crypt = RSACrypt()
        text = 'jen mám trochu pocit, že se mi chce na záchod a do koupelny, už má vytvořeny jednoduché a podle předpovědi počasí pod psa, ale celá věc za nesmírně důležité, aby se to neopakovalo a po zapracování připomínek k návrhu na prodej automobilů značky husarský kousek, když vás to tak použijeme v takové podobě, jak ji známe dnes, má na to ještě v době, kdy jsme všichni byli v pohodě, ale jak jsem si to vynahradila a pokud by se mu na ní líbilo a všechno se obrátit přímo na pobočce v brně mi vysvětlil, že je to stará fasáda, nová verze známého střediska pro koně, jednou rukou místo obvyklého pobytu nebo sídla a připravovala se na ni podívala a pak přes celé město, nebo je to jenom pro představu, co všechno musí udělat obrázek o tom, jak to vlastně všechno začalo?'
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        enc = crypt.encrypt(text, public)
        dec = crypt.decrypt(enc, private)
        self.assertTrue(dec == text)

    def test_invert_keys(self):
        crypt = RSACrypt()
        text = string.digits + string.ascii_letters
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        enc = crypt.encrypt(text, private)
        dec = crypt.decrypt(enc, public)
        self.assertTrue(dec == text)

    def test_repetitive(self):
        for _ in range(1000):
            crypt = RSACrypt()
            text = 'hello world'
            p = crypt.get_random_prime()
            q = crypt.get_random_prime()
            public, private = crypt.create_keys(p, q)
            enc = crypt.encrypt(text, private)
            dec = crypt.decrypt(enc, public)
            self.assertTrue(dec == text)

    def test_out_of_range_chars(self):
        crypt = RSACrypt()
        text = '丁Ж'
        p = crypt.get_random_prime()
        q = crypt.get_random_prime()
        public, private = crypt.create_keys(p, q)
        self.assertRaises(ValueError, crypt.encrypt, text, public)
