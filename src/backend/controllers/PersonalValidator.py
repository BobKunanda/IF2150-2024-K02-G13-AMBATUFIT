class PersonalValidator:
    @staticmethod
    def validate_usia(usia):
        """Validasi untuk usia. Harus berupa angka positif."""
        if not isinstance(usia, int) or usia <= 0:
            raise ValueError("Usia harus berupa angka positif.")
    
    @staticmethod
    def validate_tinggi(tinggi):
        """Validasi untuk tinggi badan. Harus berupa angka positif."""
        if not isinstance(tinggi, (int, float)) or tinggi <= 0:
            raise ValueError("Tinggi badan harus berupa angka positif.")
    
    @staticmethod
    def validate_berat(berat):
        """Validasi untuk berat badan. Harus berupa angka positif."""
        if not isinstance(berat, (int, float)) or berat <= 0:
            raise ValueError("Berat badan harus berupa angka positif.")
    
    @staticmethod
    def validate_tujuan(tujuan):
        """Validasi untuk tujuan kebugaran. Harus berupa string non-kosong."""
        if not isinstance(tujuan, str) or len(tujuan.strip()) == 0:
            raise ValueError("Tujuan kebugaran harus berupa string non-kosong.")
