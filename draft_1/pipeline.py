
m transformers import LlamaTokenizer, LlamaForCausalLM

# Initialize LLaMA model
tokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-2-7b")
model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b")

def query_llama(data):
    input_text = f"Analyze the following data: {data.head()}"
    
    # Query LLaMA model for insights
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=512, temperature=0.7)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example usage: Process CDR data and then query LLaMA
day_calls, night_calls = process_cdr('cdr_data.csv')
insights = query_llama(day_calls)
print(insights)

