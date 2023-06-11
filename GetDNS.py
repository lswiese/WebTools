import tkinter as tk
import dns.resolver

def collect_dns_records():
    domains = domain_entry.get().split(',')
    results = {}

    record_types = []
    if a_var.get():
        record_types.append('A')
    if mx_var.get():
        record_types.append('MX')
    if ns_var.get():
        record_types.append('NS')
    if cname_var.get():
        record_types.append('CNAME')
    if txt_var.get():
        record_types.append('TXT')

    for domain in domains:
        try:
            results[domain] = {}

            for record_type in record_types:
                answers = dns.resolver.resolve(domain.strip(), record_type)
                records = [str(rdata) for rdata in answers]
                if len(records) == 0:
                    records = ['No record']
                results[domain][record_type] = records

        except dns.resolver.NXDOMAIN:
            print(f"Domain not found: {domain}")
        except dns.resolver.NoAnswer:
            print(f"No answer for domain: {domain}")
        except dns.exception.DNSException as e:
            print(f"Error occurred for domain {domain}: {str(e)}")

    display_results(results)

def display_results(results):
    result_text.delete('1.0', tk.END)
    for domain, records in results.items():
        result_text.insert(tk.END, f"Domain: {domain}\n")
        for record_type, record_data in records.items():
            result_text.insert(tk.END, f"{record_type} records: {record_data}\n")
        result_text.insert(tk.END, "\n")

# Create the GUI
window = tk.Tk()
window.title("DNS Record Collector")

# Domain input field
domain_label = tk.Label(window, text="Enter domains (comma-separated):")
domain_label.pack()

domain_entry = tk.Entry(window)
domain_entry.pack()

# Frame for checkboxes
checkbox_frame = tk.Frame(window)
checkbox_frame.pack()

# Record type checkboxes
a_var = tk.IntVar()
a_checkbox = tk.Checkbutton(checkbox_frame, text="A", variable=a_var)
a_checkbox.pack(side=tk.LEFT, padx=5)

mx_var = tk.IntVar()
mx_checkbox = tk.Checkbutton(checkbox_frame, text="MX", variable=mx_var)
mx_checkbox.pack(side=tk.LEFT, padx=5)

ns_var = tk.IntVar()
ns_checkbox = tk.Checkbutton(checkbox_frame, text="NS", variable=ns_var)
ns_checkbox.pack(side=tk.LEFT, padx=5)

cname_var = tk.IntVar()
cname_checkbox = tk.Checkbutton(checkbox_frame, text="CNAME", variable=cname_var)
cname_checkbox.pack(side=tk.LEFT, padx=5)

txt_var = tk.IntVar()
txt_checkbox = tk.Checkbutton(checkbox_frame, text="TXT", variable=txt_var)
txt_checkbox.pack(side=tk.LEFT, padx=5)

# Collect records button
collect_button = tk.Button(window, text="Collect DNS Records", command=collect_dns_records)
collect_button.pack()

# Result display area
result_text = tk.Text(window)
result_text.pack()

window.mainloop()
