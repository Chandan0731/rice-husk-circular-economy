import customtkinter as ctk
from PIL import Image, ImageTk
import os

# --- 1. CONFIGURATION & MATH ENGINE ---
class RiceHuskMath:
    """
    Implements the 4 Governing Equations from the SATEM-2025 Paper.
    """
    def __init__(self):
        # Constants (Fixed based on Indian Standards)
        self.HUSK_RATIO = 0.22      # Ref [5]
        self.LHV = 13.5             # MJ/kg Ref [6]
        self.GEN_EFF = 0.30         # Ref [8]
        self.BIOCHAR_YIELD = 0.20   # Ref [10]
        self.EF_FLOODED = 30        # kg CH4/ha
        self.EF_AWD = 16            # kg CH4/ha
        self.PRICE_ELEC = 7.0       # INR/kWh
        self.PRICE_CHAR = 15.0      # INR/kg
        self.CAPEX_PER_KW = 80000   # INR

    def calculate(self, area, paddy_yield, gasifier_eff):
        # --- Step 1: Mass Balance ---
        total_paddy = area * paddy_yield
        total_husk = total_paddy * self.HUSK_RATIO
        
        # --- Step 2: Energy Model (Eq 2) ---
        # E = Mass * LHV * Eff_Gas * Eff_Gen
        energy_mj = total_husk * self.LHV * gasifier_eff * self.GEN_EFF
        energy_kwh = energy_mj / 3.6  # Convert MJ to kWh
        
        # --- Step 3: Biochar Model (Eq 3) ---
        biochar_kg = total_husk * self.BIOCHAR_YIELD
        
        # --- Step 4: Methane Model (Eq 1) ---
        # Delta = Area * (Flooded - AWD)
        ch4_saved = area * (self.EF_FLOODED - self.EF_AWD)
        co2_equivalent = ch4_saved * 28  # GWP of Methane is 28
        
        # --- Step 5: Economics (Eq 4) ---
        capacity_kw = energy_kwh / 1000  # Approx capacity needed
        capex = max(capacity_kw, 5) * self.CAPEX_PER_KW # Min 5kW system
        
        revenue = (energy_kwh * self.PRICE_ELEC) + (biochar_kg * self.PRICE_CHAR)
        opex = capex * 0.10 # 10% Maintenance
        profit = revenue - opex
        
        payback = capex / profit if profit > 0 else 99.9
        
        return {
            "energy": energy_kwh,
            "biochar": biochar_kg,
            "co2": co2_equivalent,
            "revenue": revenue,
            "payback": payback
        }

# --- 2. MODERN GUI CLASS ---
class ModernApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window Setup
        self.title("Rice Husk Circular Economy Simulator 2025")
        self.geometry("1100x700")
        ctk.set_appearance_mode("Dark")  # Modern Dark Mode
        ctk.set_default_color_theme("green") # Green accent for 'Eco' theme
        
        self.math_engine = RiceHuskMath()
        
        # --- BACKGROUND IMAGE SETUP ---
        # We use a Label to hold the image across the entire background
        try:
            # Load image (Ensure 'rice_field.jpg' is in the folder)
            bg_image_data = Image.open("rice_field.jpg")
            # Blur or darken image slightly in external editor for best text readability
            self.bg_image = ctk.CTkImage(bg_image_data, size=(1100, 700))
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Image not found: {e}. Using default dark background.")
            self.configure(fg_color="#1a1a1a") # Fallback color

        # --- MAIN LAYOUT (2 Columns) ---
        # Fixed: Removed 'alpha' argument which caused the error
        # Left: Controls 
        self.frame_controls = ctk.CTkFrame(self, corner_radius=20, fg_color=("white", "#2b2b2b"))
        self.frame_controls.place(relx=0.05, rely=0.1, relwidth=0.35, relheight=0.8)
        
        # Right: Results
        self.frame_results = ctk.CTkFrame(self, corner_radius=20, fg_color=("white", "#2b2b2b"))
        self.frame_results.place(relx=0.45, rely=0.1, relwidth=0.5, relheight=0.8)

        self.setup_controls()
        self.setup_results_dashboard()
        
        # Run initial calculation
        self.update_simulation()

    def setup_controls(self):
        # Title
        ctk.CTkLabel(self.frame_controls, text="Simulation Inputs", 
                     font=("Roboto", 24, "bold")).pack(pady=(30, 20))

        # --- SLIDER 1: AREA ---
        ctk.CTkLabel(self.frame_controls, text="Farm Area (Hectares)", 
                     font=("Roboto", 14)).pack(pady=(10, 0), anchor="w", padx=20)
        
        self.lbl_area = ctk.CTkLabel(self.frame_controls, text="1 Ha", font=("Roboto", 20, "bold"), text_color="#2cc985")
        self.lbl_area.pack(pady=(0, 5), anchor="e", padx=20)
        
        self.slider_area = ctk.CTkSlider(self.frame_controls, from_=1, to=100, number_of_steps=99, command=self.update_simulation)
        self.slider_area.set(1)
        self.slider_area.pack(fill="x", padx=20, pady=5)

        # --- SLIDER 2: YIELD ---
        ctk.CTkLabel(self.frame_controls, text="Paddy Yield (kg/ha)", 
                     font=("Roboto", 14)).pack(pady=(20, 0), anchor="w", padx=20)
        
        self.lbl_yield = ctk.CTkLabel(self.frame_controls, text="4500 kg", font=("Roboto", 20, "bold"), text_color="#2cc985")
        self.lbl_yield.pack(pady=(0, 5), anchor="e", padx=20)
        
        self.slider_yield = ctk.CTkSlider(self.frame_controls, from_=2000, to=8000, number_of_steps=60, command=self.update_simulation)
        self.slider_yield.set(4500)
        self.slider_yield.pack(fill="x", padx=20, pady=5)

        # --- SLIDER 3: EFFICIENCY ---
        ctk.CTkLabel(self.frame_controls, text="Gasifier Efficiency (%)", 
                     font=("Roboto", 14)).pack(pady=(20, 0), anchor="w", padx=20)
        
        self.lbl_eff = ctk.CTkLabel(self.frame_controls, text="70%", font=("Roboto", 20, "bold"), text_color="#2cc985")
        self.lbl_eff.pack(pady=(0, 5), anchor="e", padx=20)
        
        self.slider_eff = ctk.CTkSlider(self.frame_controls, from_=0.40, to=0.90, number_of_steps=50, command=self.update_simulation)
        self.slider_eff.set(0.70)
        self.slider_eff.pack(fill="x", padx=20, pady=5)

        # Credits
        ctk.CTkLabel(self.frame_controls, text="Based on SATEM-2025 Methodology", 
                     font=("Roboto", 12), text_color="gray").pack(side="bottom", pady=20)

    def setup_results_dashboard(self):
        ctk.CTkLabel(self.frame_results, text="Projected Impact", 
                     font=("Roboto", 24, "bold")).pack(pady=(30, 30))
        
        # We create 4 cards for the metrics
        self.card_energy = self.create_metric_card("⚡ Net Energy Output", "#3B8ED0")
        self.card_char = self.create_metric_card("🌱 Biochar Produced", "#E04F5F") # Red/Pink accent
        self.card_co2 = self.create_metric_card("🌍 CO2 Equivalent Avoided", "#2CC985") # Green accent
        self.card_money = self.create_metric_card("💰 Annual Profit Potential", "#E5B92E") # Gold accent
        
        # Payback special label
        self.lbl_payback = ctk.CTkLabel(self.frame_results, text="Est. Payback Period: 2.4 Years", 
                                        font=("Roboto", 16, "italic"), text_color="gray")
        self.lbl_payback.pack(pady=20)

    def create_metric_card(self, title, color):
        card = ctk.CTkFrame(self.frame_results, fg_color="transparent", border_width=2, border_color=color, corner_radius=15)
        card.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(card, text=title, font=("Roboto", 14)).pack(anchor="w", padx=15, pady=(10, 0))
        
        val_label = ctk.CTkLabel(card, text="0", font=("Roboto", 32, "bold"), text_color="white")
        val_label.pack(anchor="e", padx=20, pady=(0, 10))
        return val_label

    def update_simulation(self, event=None):
        # 1. Get Values
        area = self.slider_area.get()
        yld = self.slider_yield.get()
        eff = self.slider_eff.get()
        
        # 2. Update Labels
        self.lbl_area.configure(text=f"{int(area)} Ha")
        self.lbl_yield.configure(text=f"{int(yld)} kg")
        self.lbl_eff.configure(text=f"{int(eff*100)}%")
        
        # 3. Calculate Logic (The Math)
        results = self.math_engine.calculate(area, yld, eff)
        
        # 4. Update Result Cards
        self.card_energy.configure(text=f"{int(results['energy']):,} kWh")
        self.card_char.configure(text=f"{int(results['biochar']):,} kg")
        self.card_co2.configure(text=f"{int(results['co2']):,} kg")
        self.card_money.configure(text=f"₹ {int(results['revenue']):,}")
        
        pb = results['payback']
        if pb > 10:
            pb_text = "> 10 Years"
        else:
            pb_text = f"{pb:.1f} Years"
        self.lbl_payback.configure(text=f"Est. Payback Period: {pb_text}")

if __name__ == "__main__":
    app = ModernApp()
    app.mainloop()