import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import requests
from datetime import datetime
from fpdf import FPDF
import os

# Configurações da API
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

class PDFManual(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Cyber Sentinel - Manual de Vulnerabilidades', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()} | Gerado por Cyber Sentinel v3.0', 0, 0, 'C')

class CyberSentinelV3:
    def __init__(self, root):
        self.root = root
        self.root.title("🛡️ Cyber Sentinel v3.0 - Threat Intelligence")
        self.root.geometry("800x700")
        self.root.configure(bg="#2c3e50")

        self.last_search_results = []
        self.last_search_term = ""

        # Estilos
        self.header_font = ("Helvetica", 18, "bold")
        self.label_font = ("Helvetica", 10)
        self.text_font = ("Consolas", 10)

        self.setup_ui()

    def setup_ui(self):
        # Título
        title_label = tk.Label(self.root, text="Cyber Sentinel v3.0", font=self.header_font, fg="#ecf0f1", bg="#2c3e50", pady=20)
        title_label.pack()

        # Frame de Busca por CVE
        cve_frame = tk.LabelFrame(self.root, text="Busca por ID de CVE", font=self.label_font, fg="#3498db", bg="#2c3e50", padx=10, pady=10)
        cve_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(cve_frame, text="ID da CVE:", font=self.label_font, fg="#ecf0f1", bg="#2c3e50").pack(side=tk.LEFT, padx=5)
        self.cve_entry = tk.Entry(cve_frame, font=self.label_font, width=20)
        self.cve_entry.pack(side=tk.LEFT, padx=5)
        self.cve_entry.bind('<Return>', lambda e: self.fetch_cve_details())
        
        tk.Button(cve_frame, text="Buscar CVE", command=self.fetch_cve_details, bg="#3498db", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)

        # Frame de Busca 
        topic_frame = tk.LabelFrame(self.root, text="Busca por Assunto / Tecnologia", font=self.label_font, fg="#2ecc71", bg="#2c3e50", padx=10, pady=10)
        topic_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(topic_frame, text="Termo:", font=self.label_font, fg="#ecf0f1", bg="#2c3e50").pack(side=tk.LEFT, padx=5)
        self.topic_entry = tk.Entry(topic_frame, font=self.label_font, width=30)
        self.topic_entry.pack(side=tk.LEFT, padx=5)
        self.topic_entry.bind('<Return>', lambda e: self.search_by_topic())

        tk.Button(topic_frame, text="Pesquisar Assunto", command=self.search_by_topic, bg="#2ecc71", fg="white", relief=tk.FLAT).pack(side=tk.LEFT, padx=5)
        
        self.download_btn = tk.Button(topic_frame, text="Gerar Manual PDF", command=self.generate_pdf_manual, bg="#e67e22", fg="white", relief=tk.FLAT, state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=15)

        # Área de Resultados
        self.result_area = scrolledtext.ScrolledText(self.root, width=90, height=20, font=self.text_font, bg="#ecf0f1", fg="#2c3e50", padx=10, pady=10)
        self.result_area.pack(pady=10, padx=20)
        self.result_area.config(state=tk.DISABLED)

        # Rodapé
        footer = tk.Label(self.root, text="Cyber Sentinel v3.0 - Mateus Edition | Inteligência de Ameaças", font=("Helvetica", 8), fg="#95a5a6", bg="#2c3e50")
        footer.pack(side=tk.BOTTOM, pady=10)

    def update_result_area(self, text, clear=False):
        self.result_area.config(state=tk.NORMAL)
        if clear:
            self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, text)
        self.result_area.config(state=tk.DISABLED)

    def fetch_cve_details(self):
        cve_id = self.cve_entry.get().strip().upper()
        if not cve_id.startswith("CVE-"):
            messagebox.showwarning("Aviso", "Insira um ID de CVE válido (ex: CVE-2024-1234).")
            return

        self.update_result_area(f"Buscando {cve_id}...\n", clear=True)
        try:
            response = requests.get(NVD_API_URL, params={"cveId": cve_id}, timeout=15)
            if response.status_code == 200:
                vulnerabilities = response.json().get("vulnerabilities", [])
                if vulnerabilities:
                    self.display_cve_info(vulnerabilities[0].get("cve", {}))
                else:
                    self.update_result_area("CVE não encontrada.")
            else:
                self.update_result_area(f"Erro na API: {response.status_code}")
        except Exception as e:
            self.update_result_area(f"Erro: {str(e)}")

    def search_by_topic(self):
        term = self.topic_entry.get().strip()
        if not term:
            messagebox.showwarning("Aviso", "Digite um assunto para pesquisar.")
            return

        self.last_search_term = term
        self.update_result_area(f"Pesquisando vulnerabilidades para: '{term}'...\n", clear=True)
        
        try:
            # Busca por palavra-chave na API do NVD
            params = {"keywordSearch": term, "resultsPerPage": 10}
            response = requests.get(NVD_API_URL, params=params, timeout=15)
            
            if response.status_code == 200:
                vulnerabilities = response.json().get("vulnerabilities", [])
                self.last_search_results = vulnerabilities
                
                if not vulnerabilities:
                    self.update_result_area(f"Nenhuma vulnerabilidade encontrada para '{term}'.")
                    self.download_btn.config(state=tk.DISABLED)
                    return

                output = f"Encontradas {len(vulnerabilities)} vulnerabilidades para '{term}':\n"
                output += "="*60 + "\n\n"
                
                for item in vulnerabilities:
                    cve = item.get("cve", {})
                    cve_id = cve.get("id")
                    metrics = cve.get("metrics", {})
                    cvss_v3 = metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", [])
                    score = cvss_v3[0].get("cvssData", {}).get("baseScore", "N/A") if cvss_v3 else "N/A"
                    
                    output += f"[{cve_id}] Score: {score}\n"
                    desc = next((d.get("value") for d in cve.get("descriptions", []) if d.get("lang") == "en"), "")
                    output += f"Descrição: {desc[:150]}...\n\n"

                self.update_result_area(output)
                self.download_btn.config(state=tk.NORMAL)
            else:
                self.update_result_area(f"Erro na API: {response.status_code}")
        except Exception as e:
            self.update_result_area(f"Erro: {str(e)}")

    def display_cve_info(self, cve):
        cve_id = cve.get("id")
        desc = next((d.get("value") for d in cve.get("descriptions", []) if d.get("lang") == "en"), "")
        metrics = cve.get("metrics", {})
        cvss_v3 = metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", [])
        score = cvss_v3[0].get("cvssData", {}).get("baseScore", "N/A") if cvss_v3 else "N/A"
        
        output = f"ID: {cve_id}\nScore: {score}\n\nDescrição:\n{desc}\n"
        self.update_result_area(output, clear=True)

    def generate_pdf_manual(self):
        if not self.last_search_results:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"Manual_Seguranca_{self.last_search_term.replace(' ', '_')}.pdf"
        )

        if not file_path:
            return

        try:
            pdf = PDFManual()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"Assunto: {self.last_search_term}", 0, 1)
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 10, f"Data da Pesquisa: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
            pdf.ln(5)

            for item in self.last_search_results:
                cve = item.get("cve", {})
                cve_id = cve.get("id")
                metrics = cve.get("metrics", {})
                cvss_v3 = metrics.get("cvssMetricV31", []) or metrics.get("cvssMetricV30", [])
                score = cvss_v3[0].get("cvssData", {}).get("baseScore", "N/A") if cvss_v3 else "N/A"
                desc = next((d.get("value") for d in cve.get("descriptions", []) if d.get("lang") == "en"), "")

                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"Vulnerabilidade: {cve_id} (Score: {score})", 0, 1)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, f"Descrição: {desc}")
                
                pdf.set_text_color(0, 0, 255)
                pdf.cell(0, 10, f"Link: https://nvd.nist.gov/vuln/detail/{cve_id}", 0, 1, link=f"https://nvd.nist.gov/vuln/detail/{cve_id}")
                pdf.set_text_color(0, 0, 0)
                pdf.ln(5)

            pdf.output(file_path)
            messagebox.showinfo("Sucesso", f"Manual gerado com sucesso em:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CyberSentinelV3(root)
    root.mainloop()
