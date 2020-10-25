#Ao receber o caminho de um arquivo ".asm"
#Se não houver erros de sintaxe, este código
#converterá as C/A-instructions em binário
#gerando um arquivo "hack" de nome identico
#no mesmo caminho especificado no início.

#Autor: Lucas Spicollys Leão de Lima, 2020
#Destinado à disciplina de Elementos de Sistemas Computacionais

path = input('Insira aqui o caminho do arquivo .asm: ');
save_path = path.replace('.asm', '.hack');
asm_archive = open(path, "r")
asm_archive = asm_archive.readlines()

class Assembler(object):
	def __init__(self, asm_archive):
		self.asm_archive = asm_archive;
		self.symbol_table = {'R0': '0', 'R1': '1', 'R2': '2', 'R3': '3', 'R4': '4', 'R5': '5', 'R6': '6', 'R7': '7', 'R8': '8', 'R9': '9', 'R10': '10', 'R11': '11', 'R12': '12', 'R13': '13', 'R14': '14', 'R15': '15', 'SCREEN': '16384', 'KBD': '24576', 'SP': '0', 'LCL': '1', 'ARG': '2', 'THIS': '3', 'THAT': '4'}
		self.binary_archive = []
		self.dict_comp = {'0':'0101010','1':'0111111','-1':'0111010','D':'0001100','A':'0110000','M':'1110000','!D':'0001101','!A':'0110001','!M':'1110001','-D':'0001111','-A':'0110011','-M':'1110011','D+1':'0011111','A+1':'0110111','M+1':'1110111','D-1':'0001110','A-1':'0110010','M-1':'1110010','D+A':'0000010','D+M':'1000010','D-A':'0010011','D-M':'1010011','A-D':'0000111','M-D':'1000111','D&A':'0000000','D&M':'1000000','D|A':'0010101','D|M':'1010101'}
		self.dict_dest = {'':'000','M':'001','D':'010','MD':'011','A':'100','AM':'101','AD':'110','AMD':'111'}
		self.dict_jump = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}

	def assemble(self):
		self.translate_all_symbols();
		for i in self.asm_archive:
			if i[0] == '@':
				self.binary_archive.append(self.a_instruction_to_binary(i)+'\n');
			else:
				self.binary_archive.append(self.c_instruction_to_bynary(i)+'\n');
		return self.binary_archive;

	def remove_space_comment_linebreak(self):
		without_statements = [];
		for i in self.asm_archive:
			current_line = i[:-1].replace(' ', ''); #space removed and '\n' removed
			current_line = current_line[:current_line.index('//')] if ('//' in current_line) else current_line; #comment removed
			without_statements.append(current_line) if current_line != '' else False;
		return without_statements;

	def remove_labels(self):
		self.asm_archive = self.remove_space_comment_linebreak();
		asm_archive_without_labels = self.asm_archive.copy();
		asm_archive_indexed = [];
		index = 0;
		for i in self.asm_archive:
			if i[0] != '(':
				asm_archive_indexed.append(str(index)+'*'+i);
				index += 1;
			else:
				asm_archive_indexed.append(i);
		#adding labels to symbol table
		for i in range(len(self.asm_archive)):
			if (self.asm_archive[i][0] == '('):
				j = i
				while '*' not in asm_archive_indexed[j+1]:
					j += 1
				self.symbol_table[self.asm_archive[i][self.asm_archive[i].index('(')+1:-1]] = asm_archive_indexed[j+1][:asm_archive_indexed[j+1].index('*')];				
				asm_archive_without_labels.remove(self.asm_archive[i]);
				
		self.asm_archive = asm_archive_without_labels;

	def remove_variables(self):
		self.remove_labels()
		avaliable_location = 16;
		for i in self.asm_archive:
			if (i[0] == '@') and (not i[1:].isdigit()):
				if i[1:] not in self.symbol_table:
					self.symbol_table[i[1:]] = str(avaliable_location);
					avaliable_location += 1;

	def translate_all_symbols(self):
		self.remove_variables();
		for i in range(len(self.asm_archive)):
			if self.asm_archive[i][0] == '@' and (not self.asm_archive[i][1:].isdigit()):
				self.asm_archive[i] = '@' + self.symbol_table[self.asm_archive[i][1:]];
	
	def a_instruction_to_binary(self, a_instruction):
		integer = int(a_instruction.replace('@', ''));
		binary_number = bin(integer)[2:]
		binary_a_instruction = binary_number
		while len(binary_a_instruction) != 16:
			binary_a_instruction = '0'+ binary_a_instruction
		return binary_a_instruction

	def c_instruction_to_bynary(self, c_instruction):
		if '=' in c_instruction:
			if ';' in c_instruction:
				comp_part = c_instruction[c_instruction.index('=')+1:c_instruction.index(';')]
			else:
				comp_part = c_instruction[c_instruction.index('=')+1:]
		else:
			comp_part = c_instruction[:c_instruction.index(';')]
		dest_part = c_instruction[:c_instruction.index('=')] if ('=' in c_instruction) else '';
		jump_part = c_instruction[c_instruction.index(';')+1:] if (';' in c_instruction) else '';

		binary_c_instruction = '111'+ self.dict_comp[comp_part] + self.dict_dest[dest_part] + self.dict_jump[jump_part]
		return binary_c_instruction

foo = Assembler(asm_archive);
binary_archive = open(save_path, "a");
binary_archive.writelines(foo.assemble());
binary_archive.close();
