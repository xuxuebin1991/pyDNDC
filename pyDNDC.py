# pyDNDC.py

import re

# Site information 模块
class DNDCSiteInfo:
    def __init__(self):
        # 定义站点文件格式和默认参数
        self.default_site_information = ['Site_infomation\n',
                                        '\n',
                                        '__Site_name                                                   site_name\n',
                                        '__Simulated_years                                                     0\n',
                                        '__Latitude                                                            0\n',
                                        '__Daily_record                                                        0\n',
                                        '__Unit_system                                                         0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n']
        # 定义输入参数格式和默认值
        self.default_parameters = {'Site_name': 'site_name',
                                   'Simulated_years': 0,
                                   'Latitude': 0,
                                   'Daily_record': 0, 
                                   'Unit_system': 0}
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 进行参数替换的函数
    def set_parameters(self, parameter_dict):
        modified_table = [] # 构造一个空list，用于存放修改后的数据
        
        # 对站点名称进行替换
        if  'Site_name' in parameter_dict.keys():
            char_pattern = re.compile(r'(__Site_name\s+)(\S+)$')
            self.table = [char_pattern.sub(r'\1{}'.format(parameter_dict['Site_name']), line) for line in self.default_site_information]
        else:
            self.table = self.default_site_information
        
        # 对参数进行逐行替换    
        for i in range(len(self.table)):
            modified_line = self.table[i]
            # 正则化表达式对输入的参数值进行修改，如果没输入则保留默认值
            for parameter_name, new_value in parameter_dict.items():
                pattern = re.compile(f'(__{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))   
            # 将字符串设置为两端对齐，中间空格填充        
            modified_line_align = self.custom_align(modified_line, 72)
            modified_table.append(modified_line_align)

        return modified_table
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
# Climate 模块
class DNDCWeather:
    def __init__(self):
        # 定义默认的参数
        self.default_weather_information = ['Climate_data\n',                            
                                            '\n',
                                            '__Climate_data_type                                                   1\n',
                                            '__N_in_rainfall                                                       0\n',
                                            '__Air_NH3_concentration                                          0.0600\n',
                                            '__Air_CO2_concentration                                        420.0000\n',
                                            '__Climate_files                                                       1\n',
                                            '1                                                                 path1\n',
                                            '__Climate_file_mode                                                   0\n',
                                            '__CO2_increase_rate                                              0.0000\n',
                                            '__None                                                                0\n',
                                            '__None                                                                0\n',
                                            '__None                                                                0\n',
                                            '__None                                                                0\n',
                                            '__None                                                                0\n']
        # 定义输入参数格式和默认值 
        self.default_parameters = {'Climate_data_type': 1,
                                   'N_in_rainfall': 0,
                                   'Air_NH3_concentration': 0.06,
                                   'Air_CO2_concentration': 420, 
                                   'Climate_file_mode': 0,
                                   'CO2_increase_rate': 0
                                   }
    
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 进行参数替换的函数
    def set_parameters(self, parameter_dict, path_list):
        modified_table = []
        path_number = 1
        add_paths = False  # 跟踪何时添加路径的标志

        # # 对站点名称进行替换
        for i in range(len(self.default_weather_information)):
            modified_line = self.default_weather_information[i]

            # 检查行是否包含 '__Climate_files'
            if '__Climate_files' in modified_line:
                add_paths = True # 当含'__Climate_files'时将跟踪参数设置为True
                # 跳过现有的路径
                while '__Climate_files' not in modified_line:
                    modified_line = self.default_weather_information[i]
                    i += 1

                # 根据输入路径更新路径数
                modified_line = f'__Climate_files                                                       {len(path_list)}\n'

            # 检查行是否包含 '__Climate_file_mode'
            if '__Climate_file_mode' in modified_line:
                add_paths = False # 当含'__Climate_file_mode'时将跟踪参数设置为True
                # 添加带有编号的路径，在'__Climate_files'和'__Climate_file_mode'之间
                for path in path_list:
                    modified_table.append(f"{path_number}                                                                 {path}\n")
                    path_number += 1

            # 跳过现有路径
            if add_paths and modified_line.strip() and not modified_line.startswith('__'):
                continue

            # 对参数进行逐行替换 
            for parameter_name, new_value in parameter_dict.items():
                pattern = re.compile(f'(__{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))

            modified_line_align = self.custom_align(modified_line, 72) 
            modified_table.append(modified_line_align)

        return modified_table
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
# Soil 模块
class DNDCSoil:
    #
    def __init__(self):
        # 定义土壤文件格式和默认参数
        self.default_soil_information = ['Soil_data\n',
                                        '\n',
                                        '__Land_use_ID                                                         1\n',
                                        '__Soil_texture_ID                                                     1\n',
                                        '__Bulk_density                                                   1.0000\n',
                                        '__pH                                                             7.0000\n',
                                        '__Clay_fraction                                                  0.0300\n',
                                        '__Porosity                                                       0.3950\n',
                                        '__Bypass_flow                                                    0.0000\n',
                                        '__Field_capacity                                                 0.1500\n',
                                        '__Wilting_point                                                  0.1000\n',
                                        '__Hydro_conductivity                                             0.6336\n',
                                        '__Top_layer_SOC                                                  0.0100\n',
                                        '__Litter_fraction                                                0.0100\n',
                                        '__Humads_fraction                                                0.0184\n',
                                        '__Humus_fraction                                                 0.9716\n',
                                        '__Adjusted_litter_factor                                         1.0000\n',
                                        '__Adjusted_humads_factor                                         1.0000\n',
                                        '__Adjusted_humus_factor                                          1.0000\n',
                                        '__Humads_C/N                                                    10.0000\n',
                                        '__Humus_C/N                                                     10.0000\n',
                                        '__Black_C                                                        0.0000\n',
                                        '__Black_C_C/N                                                  500.0000\n',
                                        '__SOC_profile_A                                                  0.0800\n',
                                        '__SOC_profile_B                                                  1.4000\n',
                                        '__Initial_nitrate_ppm                                            0.5000\n',
                                        '__Initial_ammonium_ppm                                           0.0500\n',
                                        '__Soil_microbial_index                                           1.0000\n',
                                        '__Soil_slope                                                     0.0000\n',
                                        '__Lateral_influx_index                                           1.0000\n',
                                        '__Watertable_depth                                               1.0000\n',
                                        '__Water_retension_layer_depth                                    9.9900\n',
                                        '__Soil_salinity                                                  0.0000\n',
                                        '__SCS_curve_use                                                       0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n',
                                        '__None                                                                0\n']
        # 定义部分输入参数格式和默认值
        self.default_parameters = {'Land_use_ID': 0, 
                                   'Soil_texture_ID': 1,
                                   'Bulk_density': 1,
                                   'pH': 7,
                                   'Top_layer_SOC': 0.01,
                                   'Initial_nitrate_ppm': 0.5000,
                                   'Initial_ammonium_ppm': 0.0500,
                                    'Soil_microbial_index': 1,
                                    'Soil_slope': 0,
                                    'Water_retension_layer_depth': 9.99,
                                    'Soil_salinity': 0}

        self.table = self.default_soil_information
        
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 进行参数替换的函数 
    def set_parameters(self, parameter_dict=None):
        # 检测是否输入参数，否则报错
        if parameter_dict is None:
            raise ValueError("Please provide a parameter dictionary.")
        
        # 检查是否输入土地利用方式，否则报错
        if 'Land_use_ID' not in parameter_dict:
            raise ValueError("Please define 'Land_use_ID' in the parameter dictionary.")

        # 检查是否输入土壤质地，否则报错
        if 'Soil_texture_ID' not in parameter_dict:
            raise ValueError("Please define 'Soil_texture_ID' in the parameter dictionary.")

        # 使用预定义的土壤参数映射土壤质地
        soil_texture_id = parameter_dict['Soil_texture_ID']
        texture_mapping = self.get_parameters_from_texture(soil_texture_id)
        
        for param_name_texture, param_value_texture in texture_mapping.items():
            if param_name_texture not in parameter_dict.keys():
                parameter_dict[param_name_texture] = param_value_texture
       
        # 检查是否输入土壤有机质含量，否则报错
        if 'Top_layer_SOC' not in parameter_dict:
            raise ValueError("Please define 'Top_layer_SOC' in the parameter dictionary.")
        
        # 使用默认soc的预定义映射对 'Litter_fraction', 'Humads_fraction', 'Humus_fraction'参数赋值
        params_fraction = ['Litter_fraction', 'Humads_fraction', 'Humus_fraction']
        if not all(param in parameter_dict for param in params_fraction):
            print('The input parameters of soc fraction is insufficient, using defaut values !')
            soc_content = parameter_dict['Top_layer_SOC']
            soc_mapping = self.get_parameters_from_soc(soc_content)     
            parameter_dict.update(soc_mapping)       
        else:
            if  sum([parameter_dict[key] for key in params_fraction]) != 1:
                raise ValueError("The total fraction is not 1, please ensure the total fraction is 1")
        
        modified_table = []           
        # 对参数进行逐行替换
        for i in range(len(self.table)):
            modified_line = self.table[i]

            for parameter_name, new_value in parameter_dict.items():
                pattern = re.compile(f'(__{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            
            modified_line_align = self.custom_align(modified_line, 72) # 将字符串设置为两端对齐，中间空格填充
            modified_table.append(modified_line_align)

        return modified_table
    
    # 用于土壤质地映射的函数
    def get_parameters_from_texture(self, soil_texture_id):
        # 土壤质地映射表
        texture_mapping = {
            1: {'Clay_fraction': 0.0300, 'Field_capacity': 0.1500, 'Wilting_point': 0.1000, 'Hydro_conductivity': 0.6336, 'Porosity': 0.3950},
            2: {'Clay_fraction': 0.0600, 'Field_capacity': 0.2500, 'Wilting_point': 0.1300, 'Hydro_conductivity': 0.5628, 'Porosity': 0.4110},
            3: {'Clay_fraction': 0.0900, 'Field_capacity': 0.3200, 'Wilting_point': 0.1500, 'Hydro_conductivity': 0.1248, 'Porosity': 0.4350},
            4: {'Clay_fraction': 0.1400, 'Field_capacity': 0.400, 'Wilting_point': 0.2000, 'Hydro_conductivity': 0.02592, 'Porosity': 0.4850},
            5: {'Clay_fraction': 0.1900, 'Field_capacity': 0.4900, 'Wilting_point': 0.2200, 'Hydro_conductivity': 0.02502, 'Porosity': 0.4510},
            6: {'Clay_fraction': 0.2700, 'Field_capacity': 0.5200, 'Wilting_point': 0.2400, 'Hydro_conductivity': 0.02268, 'Porosity': 0.4210},
            7: {'Clay_fraction': 0.3400, 'Field_capacity': 0.5500, 'Wilting_point': 0.2600, 'Hydro_conductivity': 0.0150, 'Porosity': 0.4770},
            8: {'Clay_fraction': 0.4100, 'Field_capacity': 0.5700, 'Wilting_point': 0.2700, 'Hydro_conductivity': 0.00882, 'Porosity': 0.4760},
            9: {'Clay_fraction': 0.4300, 'Field_capacity': 0.6000, 'Wilting_point': 0.2800, 'Hydro_conductivity': 0.0080, 'Porosity': 0.4260},
            10: {'Clay_fraction': 0.4900, 'Field_capacity': 0.6300, 'Wilting_point': 0.3000, 'Hydro_conductivity': 0.0080, 'Porosity': 0.4920},
            11: {'Clay_fraction': 0.6300, 'Field_capacity': 0.7500, 'Wilting_point': 0.4500, 'Hydro_conductivity': 0.0080, 'Porosity': 0.4820},
            12: {'Clay_fraction': 0.0600, 'Field_capacity': 0.5500, 'Wilting_point': 0.2600, 'Hydro_conductivity': 0.0080, 'Porosity': 0.7010}
        }
        return texture_mapping.get(soil_texture_id, {})
    
    # 用于土壤有机质组分映射的函数
    def get_parameters_from_soc(self, soc_content):
        # 默认的土壤有机质组分映射表
        litter_fraction = 0.01           
        humads_fraction = 0.4611 * soc_content + 0.0138
        humus_fraction = 1 - litter_fraction - humads_fraction
        soc_mapping = {
            'Litter_fraction': litter_fraction,
            'Humads_fraction': humads_fraction,
            'Humus_fraction': humus_fraction
        }
        return soc_mapping
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Crop 子模块
class DNDCCrop:
    # 定义作物文件格式和默认参数
    def __init__(self):
        self.crop_number = ['____Crops                                                             1\n']
        self.default_crop_information = ['______Crop#                                                           1\n',
                                        '______Crop_ID                                                        20\n',
                                        '______Planting_month                                                  4\n',
                                        '______Planting_day                                                    1\n',
                                        '______Harvest_month                                                   6\n',
                                        '______Harvest_day                                                    30\n',
                                        '______Harvest_year                                                    1\n',
                                        '______Residue_left_in_field                                      0.0000\n',
                                        '______Maximum_yield                                           3377.5801\n',
                                        '______Leaf_fraction                                              0.2300\n',
                                        '______Stem_fraction                                              0.2400\n',
                                        '______Root_fraction                                              0.1200\n',
                                        '______Grain_fraction                                             0.4100\n',
                                        '______Leaf_C/N                                                  85.0000\n',
                                        '______Stem_C/N                                                  85.0000\n',
                                        '______Root_C/N                                                  85.0000\n',
                                        '______Grain_C/N                                                 45.0000\n',
                                        '______Accumulative_temperature                                2000.0000\n',
                                        '______Optimum_temperature                                       25.0000\n',
                                        '______Water_requirement                                        508.0000\n',
                                        '______N_fixation_index                                           1.0500\n',
                                        '______Vascularity                                                1.0000\n',
                                        '______If_cover_crop                                                   0\n',
                                        '______If_perennial_crop                                               0\n',
                                        '______If_transplanted                                                 1\n',
                                        '______Tree_maturity_age                                 -107374000.0000\n',
                                        '______Tree_current_age                                           0.0000\n',
                                        '______Tree_max_leaf                                              0.0000\n',
                                        '______Tree_min_leaf                                              0.0000\n',
                                        '______None                                                            0\n',
                                        '______None                                                            0\n',
                                        '______None                                                            0\n',
                                        '______None                                                            0\n',
                                        '______None                                                            0\n',
                                        '______None                                                            0\n',
                                        '______None                                                            0\n',
                                        '\n']
        # 定义默认的作物参数
        self.default_crop = {0:{'Maximum_yield': 0,
                                'Leaf_fraction': 0.25,
                                'Stem_fraction': 0.25,
                                'Root_fraction': 0.4,
                                'Grain_fraction': 0.1,
                                'Leaf_C/N': 1,
                                'Stem_C/N': 1,
                                'Root_C/N': 1,
                                'Grain_C/N': 1,
                                'Accumulative_temperature': 0,
                                'Optimum_temperature': 20,
                                'Water_requirement': 0,
                                'N_fixation_index': 1,
                                'Vascularity': 0},
                            1: {'Maximum_yield': 4123.6,
                                'Leaf_fraction': 0.22,
                                'Stem_fraction': 0.22,
                                'Root_fraction': 0.16,
                                'Grain_fraction': 0.4,
                                'Leaf_C/N': 80,
                                'Stem_C/N': 80,
                                'Root_C/N': 80,
                                'Grain_C/N': 50,
                                'Accumulative_temperature': 2550.0000,
                                'Optimum_temperature': 30.0000,
                                'Water_requirement': 150.0000,
                                'N_fixation_index': 1.0000,
                                'Vascularity': 0},
                            2: {'Maximum_yield': 3120.1,
                                'Leaf_fraction': 0.21,
                                'Stem_fraction': 0.21,
                                'Root_fraction': 0.17,
                                'Grain_fraction': 0.41,
                                'Leaf_C/N': 95,
                                'Stem_C/N': 95,
                                'Root_C/N': 95,
                                'Grain_C/N': 40,
                                'Accumulative_temperature': 1300.0000,
                                'Optimum_temperature': 22.0000,
                                'Water_requirement': 200.0000,
                                'N_fixation_index': 1.0000,
                                'Vascularity': 0},
                            20: {'Maximum_yield': 3377.58,
                                'Leaf_fraction': 0.23,
                                'Stem_fraction': 0.24,
                                'Root_fraction': 0.12,
                                'Grain_fraction': 0.41,
                                'Leaf_C/N': 85,
                                'Stem_C/N': 85,
                                'Root_C/N': 85,
                                'Grain_C/N': 45,
                                'Accumulative_temperature': 2000.0000,
                                'Optimum_temperature': 25.0000,
                                'Water_requirement': 2000.0000,
                                'N_fixation_index': 1.0500,
                                'Vascularity': 1},
                            }
        
        # 定义输入参数格式和默认值
        self.default_parameters = {1: {'Planting_month': 1,
                                   'Planting_day': 1,
                                   'Harvest_month': 1,
                                   'Harvest_day': 1, 
                                   'Harvest_year': 0,
                                   'Residue_left_in_field': 1,
                                   'Maximum_yield': '-',
                                   'If_cover_crop': 0,
                                   'If_perennial_crop': 0, 
                                   'If_transplanted': 1,
                                   }}
        
        self.table = self.default_crop_information
    
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 进行参数替换的函数 
    def set_parameters(self, parameter_dict=None):
        # 检查是否输入参数
        if parameter_dict is None:
            raise ValueError("Please provide a parameter dictionary.")              
 
        modified_list = []
        times= len(parameter_dict)
        modified_crop_number = [line.replace('1', str(times)) for line in self.crop_number]
        for crop_num, sub_parameters_dict in parameter_dict.items():
            # 检查Crop_ID是否输入
            if 'Crop_ID' not in sub_parameters_dict:
                raise ValueError("Please define 'Crop_ID' in the parameter dictionary.")

            # 检查输入作物的参数是否在默认数据中，如果没有则用户需要手动添加
            if sub_parameters_dict['Crop_ID'] not in self.default_crop.keys():
                raise ValueError("There is no defaut values for your crop, please define crop parameters. Your can refer to  http://www.dndc.sr.unh.edu/model/GuideDNDC95.pdf")
            
            # 为输入的作为设置默认的作物参数
            crop_id = sub_parameters_dict['Crop_ID']
            crop_mapping = self.default_crop.get(crop_id, {})
            for param_name, param_value in crop_mapping.items():
                if param_name not in parameter_dict.keys():
                    sub_parameters_dict[param_name] = param_value    
            
            first_string = self.table[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(crop_num), first_string, count=1)
            modified_table = self.modify(self.table[1:], sub_parameters_dict)
            modified_list.extend([result] + modified_table)
        modified = modified_crop_number + modified_list
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
   
        # 定义一个修改参数的函数        
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_table.append(modified_line)
        return modified_table
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Tillage 子模块
class DNDCTillage:
    # 定义站点文件格式和默认参数
    def __init__(self):   
        self.default_tillage_applications = ['____Till_applications                                                 1\n']
        self.default_tillage_informations = ['______Till#                                                           1\n',
                                        '______Till_month                                                      1\n',
                                        '______Till_day                                                        1\n',
                                        '______Till_method                                                     1\n']
        
        self.default_parameters = {1: {'Till_month': 1,
                                        'Till_day': 1,
                                        'Till_method': 1}}

        self.tillage_applications = self.default_tillage_applications
        self.tillage_informations = self.default_tillage_informations
    
    # 进行参数替换的函数
    def set_parameters(self, parameter_dict):
        modified_list = []
        times= len(parameter_dict)
        modified_tillage_application = [line.replace('1', str(times)) for line in self.tillage_applications]
        for tillage_times, sub_parameters_dict in parameter_dict.items():
            first_string = self.default_tillage_informations[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(tillage_times), first_string, count=1)
            modified_table = self.modify(self.default_tillage_informations[1:], sub_parameters_dict)
            modified_list.extend([result] + modified_table)
        modified = modified_tillage_application + modified_list
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
    
    # 定义一个修改参数的函数        
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_table.append(modified_line)
        return modified_table
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Fertilizer 子模块
class DNDCFertilizer:
    # 定义施肥文件格式和默认参数
    def __init__(self):
        self.default_manual_fertilization_application = ['____Fertilizer_applications                                           1\n']
        self.default_manual_fertilization_informations = ['______Fertilizing#                                                    1\n',
                                                         '______Fertilizing_month                                               1\n',
                                                         '______Fertilizing_day                                                 1\n',
                                                         '______Fertilizing_method                                              0\n',
                                                         '______Fertilizing_depth                                          0.0000\n',
                                                         '______Nitrate                                                    0.0000\n',
                                                         '______Ammonium_bicarbonate                                       0.0000\n',
                                                         '______Urea                                                       0.0000\n',
                                                         '______Anhydrous_ammonia                                          0.0000\n',
                                                         '______Ammonium                                                   0.0000\n',
                                                         '______Sulphate                                                   0.0000\n',
                                                         '______Phosphate                                                  0.0000\n',
                                                         '______Slow_release_rate                                          1.0000\n',
                                                         '______Nitrification_inhibitor_efficiency                         0.0000\n',
                                                         '______Nitrification_inhibitor_duration                           0.0000\n',
                                                         '______Urease_inhibitor_efficiency                                0.0000\n',
                                                         '______Urease_inhibitor_duration                                  0.0000\n',
                                                         '______None                                                            0\n',
                                                         '______None                                                            0\n',
                                                         '______None                                                            0\n',
                                                         '______None                                                            0\n',
                                                         '______None                                                            0\n']
        self.auto_fertilization = ['____Fertilizer_applications                                          -2\n',
                                   '____Fertilization_option                                              0\n']
        self.precision_fertilization = ['____Fertilizer_applications                                          -3\n',
                                        '____Fertilization_option                                              0\n']
        self.fertig_fertilization = ['____Fertilizer_applications                                          -1\n',
                                     '______Fertilization_file                                           path\n']
        
        self.default_none = ['____Fertilizer_applications                                           0\n',
                             '____Fertilization_option                                              0\n']
        
        # 定义输入参数格式和默认值
        self.default_parameters = {1: {'Fertilizing_month': 1,
                                        'Fertilizing_day': 1,
                                        'Fertilizing_method': 0,
                                        'Fertilizing_depth': 0,
                                        'Nitrate': 0,
                                        'Ammonium_bicarbonate': 0,
                                        'Urea': 1,
                                        'Anhydrous_ammonia': 1,
                                        'Ammonium': 0,
                                        'Sulphate': 0,
                                        'Phosphate': 0,
                                        'Slow_release_rate': 1,
                                        'Nitrification_inhibitor_efficiency': 1,
                                        'Nitrification_inhibitor_duration': 0,
                                        'Urease_inhibitor_efficiency': 0,
                                        'Urease_inhibitor_duration': 0}}
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 进行参数替换的操作函数
    def process_fertilization(self, mode, parameter_dict=None):
        # 判断是那种施肥模式，分别进行不同的操作
        if mode == 'none':
            return self.default_none
        if mode == 'manual':
            return self.process_manual_fertilization(parameter_dict)
        elif mode == 'auto':
            return self.process_auto_fertilization()
        elif mode == 'precision':
            return self.process_precision_fertilization()
        elif mode == 'fertig':
            return self.process_fertig_fertilization(parameter_dict)
        else:
            raise ValueError("Invalid fertilization mode")

    # 定义一个手动施肥参数修改函数
    def process_manual_fertilization(self, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a fertilization dictionary for manual mode.")
        modified_manual_fertilization = self.set_parameters(parameter_dict)
        return modified_manual_fertilization
    
    # 定义一个自动施肥参数修改函数
    def process_auto_fertilization(self):
        # Process and modify the auto_fertilization based on the requirements for auto mode
        modified_auto_fertilization = self.auto_fertilization
        return modified_auto_fertilization
    
    # 定义一个精准施肥参数修改函数
    def process_precision_fertilization(self):
        # Process and modify the precision_fertilization based on the requirements for precision mode
        modified_precision_fertilization = self.precision_fertilization
        return modified_precision_fertilization
    
    # 定义一个按照施肥表进行施肥的修改函数
    def process_fertig_fertilization(self, parameter_dict):
        if not parameter_dict:
            raise ValueError("Please provide a valid path for fertig mode.")
        modified_fertig_fertilization = []
        # Process and modify the fertig_fertilization based on the requirements for fertig mode
        for line in self.fertig_fertilization:
            modified_line = line.replace('path', str(parameter_dict.values()))
            modified_fertig_fertilization.append(modified_line)
            
    # 定义一个参数修改函数
    def set_parameters(self, parameter_dict):
        modified_list = []
        times= len(parameter_dict)
        modified_fertilization_application = [line.replace('1', str(times)) for line in self.default_manual_fertilization_application]
        for fertilizer_times, sub_parameters_dict in parameter_dict.items():
            first_string = self.default_manual_fertilization_informations[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(fertilizer_times), first_string, count=1)
            modified_table = self.modify(self.default_manual_fertilization_informations[1:], sub_parameters_dict)
            modified_list.extend([result] + modified_table)
        modified = modified_fertilization_application + modified_list
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
    
    # 定义一个子参数修改的函数        
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_table.append(modified_line)
        return modified_table
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Manure 子模块
class DNDCManure:
    # 定义有机肥文件格式和默认参数
    def __init__(self):
        self.default_manure_applications = ['____Manure_applications                                               1\n']
        self.default_manure_informations = ['______Manuring#                                                       1\n',
                                            '______Manuring_month                                                  1\n',
                                            '______Manuring_day                                                    1\n',
                                            '______Manure_amount                                                   0\n',
                                            '______Manure_C/N                                                13.0000\n',
                                            '______Manure_type                                                     1\n',
                                            '______Manuring_method                                                 0\n',
                                            '______Manure_depth                                               0.0000\n',
                                            '______Manure_OrgN                                                0.0000\n',
                                            '______Manure_NH4                                                 0.0000\n',
                                            '______Manure_NO3                                                 0.0000\n',
                                            '______None                                                            0\n']
        self.without_manure = ['____Manure_applications                                               0\n']
        self.default_parameters = {1: {'Manuring_month': 1,
                                        'Manuring_day': 1,
                                        'Manure_amount': 0,
                                        'Manure_C/N': 0, 
                                        'Manure_type': 0,
                                        'Manuring_method': 0,
                                        'Manure_depth': 0,
                                        'Manure_OrgN': 0,
                                        'Manure_NH4': 0,
                                        'Manure_NO3': 0}}
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 定义有机肥参数修改操作
    def process_manure(self, mode, parameter_dict=None):
        # 判断是否施用有机肥
        if mode == 'none':
            return self.without_manure
        elif mode == 'manure':
            return self.process_manure_fertilization(parameter_dict)
        else:
            raise ValueError("Invalid manure mode")
        
    # 定义有机肥施用参数修改函数
    def process_manure_fertilization(self, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a manure dictionary for manual mode.")
        modified_manure_fertilization = self.set_parameters(parameter_dict)
        return modified_manure_fertilization    
    
    # 定义参数修改函数
    def set_parameters(self, parameter_dict):               
        modified_list = []
        times= len(parameter_dict)
        modified_manure_application = [line.replace('1', str(times)) for line in self.default_manure_applications]
        for manure_times, sub_parameters_dict in parameter_dict.items():
            # 判断是否输入有机肥类型
            if 'Manure_type' not in sub_parameters_dict:
                raise ValueError("Please define 'Manure_type' in the parameter dictionary.")
            # 施用默认的有机肥参数进行映射
            Manure_type = sub_parameters_dict['Manure_type']
            manure_mapping = self.get_manure_cn_ratio(Manure_type)
            for param_name_manure, param_value_manure in manure_mapping.items():
                if param_name_manure not in sub_parameters_dict.keys():
                    sub_parameters_dict[param_name_manure] = param_value_manure
            
            sub_parameters_dict.update(self.get_nutrients_from_manure(sub_parameters_dict))
                
            first_string = self.default_manure_informations[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(manure_times), first_string, count=1)
            modified_table = self.modify(self.default_manure_informations[1:], sub_parameters_dict)
            
            modified_list.extend([result] + modified_table)
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified_list:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
    
    # 定义参数修改方法    
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_table.append(modified_line)
        return modified_table
    
    # 定义有机肥CN比映射方法
    def get_manure_cn_ratio(self, Manure_type):
        # Manure mapping table
        manure_mapping = {
            1: {'Manure_C/N': 13},
            2: {'Manure_C/N': 25},
            3: {'Manure_C/N': 70},
            4: {'Manure_C/N': 5},
            5: {'Manure_C/N': 30},
            6: {'Manure_C/N': 2},
            7: {'Manure_C/N': 5},
            8: {'Manure_C/N': 9.5},
            9: {'Manure_C/N': 5.6},
            10: {'Manure_C/N': 4}
        }
        return manure_mapping.get(Manure_type, {})
    
    # 定义有机肥性质映射方法
    def get_nutrients_from_manure(self, sub_parameters_dict):
        # defaut nutrients mapping table
        Manure_amount = sub_parameters_dict['Manure_amount']
        Manure_CN = sub_parameters_dict['Manure_C/N']
        Manure_OrgN = Manure_amount / Manure_CN
        if sub_parameters_dict['Manure_type'] in [2, 3, 6]:
            Manure_NH4 = 0
            Manure_NO3 = 0
        if sub_parameters_dict['Manure_type'] in [5]:
            Manure_NH4 = Manure_OrgN * 0.5
            Manure_NO3 = Manure_NH4
        if sub_parameters_dict['Manure_type'] in [7]:
            Manure_NH4 = Manure_OrgN * 0.5
            Manure_NO3 = Manure_NH4 * 0.4
        if sub_parameters_dict['Manure_type'] in [8]:
            Manure_NH4 = Manure_OrgN * 0.6
            Manure_NO3 = Manure_NH4 * 0.6667
        if sub_parameters_dict['Manure_type'] in [9]:
            Manure_NH4 = Manure_OrgN * 0.2
            Manure_NO3 = Manure_NH4 * 0.5
        if sub_parameters_dict['Manure_type'] in [10]:
            Manure_NH4 = Manure_OrgN * 0.1
            Manure_NO3 = 0
        if sub_parameters_dict['Manure_type'] in [1, 4]:    
            Manure_NH4 = Manure_OrgN * 0.1
            Manure_NO3 = Manure_NH4 * 0.4
        nutrients_mapping = {
            'Manure_OrgN': round(Manure_OrgN, 4),
            'Manure_NH4': round(Manure_NH4, 4),
            'Manure_NO3': round(Manure_NO3, 4)
        }
        return nutrients_mapping
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Irrigation 子模块
class DNDCIrrigation:
    # 定义灌溉文件格式和默认参数
    def __init__(self):
        self.default_events_irrigation_application = ['____Irrigation_applications                                           1\n']
        self.default_events_irrigation_informations = ['____Irrigation_control                                                0\n',
                                                        '____Irrigation_index                                             0.0000\n',
                                                        '____Irrigation_method                                                 0\n',
                                                        '______Irrigation#                                                     1\n',
                                                        '______Irri_month                                                      1\n',
                                                        '______Irri_day                                                        1\n',
                                                        '______Water_amount                                              10.0000\n',
                                                        '______Irri_method                                                     0\n',
                                                        '______None                                                            0\n',
                                                        '______None                                                            0\n',
                                                        '______None                                                            0\n',
                                                        '______None                                                            0\n',
                                                        '______None                                                            0\n']
        self.irrigation_index = ['____Irrigation_applications                                           0\n',
                                 '____Irrigation_control                                                1\n',
                                 '____Irrigation_index                                             0.0000\n',
                                 '____Irrigation_method                                                 0\n']
        self.default_none = ['____Irrigation_applications                                           0\n',
                                 '____Irrigation_control                                                0\n',
                                 '____Irrigation_index                                             0.0000\n',
                                 '____Irrigation_method                                                 0\n']
        
        self.default_parameters_index = {1: {'Irrigation_index': 0,
                                             'Irrigation_method': 0}}
        self.default_parameters_events = {1: {'Irri_month': 0,
                                              'Irri_day': 0, 
                                              'Water_amount': 0,
                                              'Irri_method': 0,}}
    # 获取默认参数的函数
    def get_default_parameters(self, mode=None):
        if mode == None:
            raise ValueError('Please input irrigation mode: "index" or "events".')
        elif mode == 'index':
            return self.default_parameters_index
        elif mode == 'events':
            return self.default_parameters_events
        else: 
            raise ValueError('Please input right irrigation mode: "index" or "events".')
    
    # 进行参数替换操作的函数
    def process_irrigation(self, mode, parameter_dict=None):
        if mode == 'none':
            return self.default_none
        if mode == 'events':
            return self.process_events_irrigation(parameter_dict)
        elif mode == 'index':
            return self.process_index_irrigation(parameter_dict)
        else:
            raise ValueError("Invalid irrigation mode")
        
    # 定义根据事灌溉的函数
    def process_events_irrigation(self, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a irrigation events for events irrigation.")
        if not self.is_nested_dict(parameter_dict):
            raise ValueError("In input error, your input a irrigation index for events. Please provide a irrigation events for events irrigation.")        
        modified_events_irrigation = self.set_parameters(parameter_dict)
        return modified_events_irrigation
    
    # 定义根据灌溉指数的函数
    def process_index_irrigation(self, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a irrigation index dictionary for index irrigation.")
        if self.is_nested_dict(parameter_dict):
            raise ValueError("In input error, your input a irrigation events for index. Please provide a irrigation index dictionary for index irrigation.")
        if not (0 <= parameter_dict['Irrigation_index'] <=1):
            raise ValueError("Irrigation index needs to be between 0 and 1 !")
        if parameter_dict['Irrigation_method'] not in [0,1,2,3]:
            raise ValueError("Irrigation method error. 0-Furrow，1-Sprinkler，2-Drip(0cm)，3-Drip(15cm)")
        modified_index_irrigation = self.set_parameters_index_irrigation(parameter_dict)
        return modified_index_irrigation
    
    # 定义参数修改函数
    def set_parameters(self, parameter_dict):
        modified_list = []
        times= len(parameter_dict)
        modified_irrigation_application = [line.replace('1', str(times)) for line in self.default_events_irrigation_application]
        for irrigation_times, sub_parameters_dict in parameter_dict.items():
            if sub_parameters_dict['Irri_method'] not in [0,1,2,3]:
                raise ValueError("Irrigation method error. 0-Furrow，1-Sprinkler，2-Drip(0cm)，3-Drip(15cm)")
            
            first_string = self.default_events_irrigation_informations[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(irrigation_times), first_string, count=1)
            modified_table = self.modify(self.default_events_irrigation_informations[1:], sub_parameters_dict)
            modified_list.extend([result] + modified_table)
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified_list:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
    
    # 定义子参数修改的函数        
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_line_align = self.custom_align(modified_line, 72)
            modified_table.append(modified_line_align)
        return modified_table
    
    # 定义基于灌溉指数的参数修改函数
    def set_parameters_index_irrigation(self, parameter_dict):
        modified_table = []
        for i in range(len(self.irrigation_index)):
            modified_line = self.irrigation_index[i]
            
            for parameter_name, new_value in parameter_dict.items():
                pattern = re.compile(f'(____{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))  
            modified_line_align = self.custom_align(modified_line, 72)
            modified_table.append(modified_line_align)
        return modified_table
    
    # 定义判断函数
    def is_nested_dict(self, input_dict):
        if isinstance(input_dict, dict):
            for value in input_dict.values():
                if isinstance(value, dict):
                    return True
        return False
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Flooding 子模块
class DNDCFlooding:
    # 定义默认格式
    def __init__(self):
        self.default_flooding_application = ['____Flood_applications                                                0\n',
                                                '____Water_control                                                     0\n',
                                                '____Flood_water_N                                                0.0000\n',
                                                '____Leak_rate                                                    0.0000\n',
                                                '____Water_gather_index                                           1.0000\n',
                                                '____Watertable_file                                                None\n',
                                                '____Empirical_para_1                                             0.0000\n',
                                                '____Empirical_para_2                                             0.0000\n',
                                                '____Empirical_para_3                                             0.0000\n',
                                                '____Empirical_para_4                                             0.0000\n',
                                                '____Empirical_para_5                                             0.0000\n',
                                                '____Empirical_para_6                                             0.0000\n']
        
        self.default_flooding_informations = ['______Flooding#                                                       1\n',
                                                '______Start_month                                                     1\n',
                                                '______Start_day                                                       1\n',
                                                '______End_month                                                       1\n',
                                                '______End_day                                                         1\n',
                                                '______Water_N                                                    0.0000\n',
                                                '______Alter_wet_dry                                                   0\n',
                                                '______None                                                            0\n',
                                                '______None                                                            0\n',
                                                '______None                                                            0\n',
                                                '______None                                                            0\n',
                                                '______None                                                            0\n']
        # 定义输入参数格式和默认值
        self.default_parameters_scheduled = {1:{'Start_month': 1,
                                                'Start_day': 1,
                                                'End_month': 1,
                                                'End_day': 1, 
                                                'Water_N': 0,
                                                'Alter_wet_dry': 0,
                                                'Flood_water_N': 0,
                                                'Leak_rate': 1}
                                                    }
        self.default_parameters_rainfed = {1: {'Water_gather_index': 1,
                                               'Flood_water_N': 0,
                                               'Leak_rate': 1}
                                                    }
        self.default_parameters_observed = {1: {'Watertable_file': 'path',
                                               'Flood_water_N': 0,
                                               'Leak_rate': 1}
                                                    }
        self.default_parameters_empirical = {1: {'Empirical_para_1': 0,
                                                 'Empirical_para_2': 0,
                                                 'Empirical_para_3': 0,
                                                 'Empirical_para_4': 0,
                                                 'Empirical_para_5': 0,
                                                 'Empirical_para_6': 0,
                                                 'Flood_water_N': 0,
                                                 'Leak_rate': 1}
                                                    }
    # 获取默认参数的函数
    def get_default_parameters(self, mode=None):
        if mode == None:
            raise ValueError('Please input flooding mode: "scheduled", "rainfed", "observed", or "empirical".')
        elif mode == 'scheduled':
            return self.default_parameters_scheduled
        elif mode == 'rainfed':
            return self.default_parameters_rainfed
        elif mode == 'observed':
            return self.default_parameters_observed
        elif mode == 'empirical':
            return self.default_parameters_empirical
        else: 
            raise ValueError('Please input right flooding mode: "scheduled", "rainfed", "observed", or "empirical".')
    
    # 定义储量flooding的函数
    def process_flooding(self, mode, parameter_dict=None):
        if mode == 'none':
            return self.default_flooding_application
        if mode == 'scheduled':
            return self.process_scheduled_flooding(parameter_dict)
        elif mode in ['rainfed', 'observed', 'empirical']:
            return self.process_others_flooding(mode, parameter_dict)
        else:
            raise ValueError("Invalid flooding mode")

    # 定义scheduled_flooding处理函数
    def process_scheduled_flooding(self, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a flooding events for flooding.")
        if not self.is_nested_dict(parameter_dict):
            raise ValueError("In input error. Please provide a flooding events for flooding.")
        
        modified_scheduled_flooding = self.set_parameters(parameter_dict)
        return modified_scheduled_flooding
    
    # 定义其他flooding处理函数
    def process_others_flooding(self, mode, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a flooding dictionary for rainfed flooding.")
        if self.is_nested_dict(parameter_dict):
            raise ValueError("In input error, your input flooding scheduled for rainfed.")
       
        modified_others_flooding = self.set_parameters_others(mode, parameter_dict)
        return modified_others_flooding
    
    # 定义参数修改函数
    def set_parameters(self, parameter_dict):       
        modified_list = []
        times= len(parameter_dict)
        modified_flooding_application = self.default_flooding_application
        flooding_application_first = self.default_flooding_application[0]
        pattern_first = re.compile(r'(\d+\.?\d*)')        
        modified_flooding_application_first = pattern_first.sub(str(times), flooding_application_first)
        modified_flooding_application[0] = modified_flooding_application_first
        
        for flooding_times, sub_parameters_dict in parameter_dict.items():
            if not sub_parameters_dict['Alter_wet_dry'] in [0, 1]:
                raise ValueError("Alter wet dry must be 0 or 1. 0-Continuous flooding (10cm), 1-Alter wet dry (-5~5cm).")
            
            first_string = self.default_flooding_informations[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(flooding_times), first_string, count=1)
            modified_table = self.modify(self.default_flooding_informations[1:], sub_parameters_dict)
            modified_list.extend([result] + modified_table)
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified_list:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
    
    # 定义子参数修改函数        
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_line_align = self.custom_align(modified_line, 72)
            modified_table.append(modified_line_align)
        return modified_table
    
    # 定义其他flooding的参数修改函数
    def set_parameters_others(self, mode, parameter_dict):
        if mode == 'rainfed':
            parameter_dict.update({'Water_control': 1})
        elif mode == 'observed':
            parameter_dict.update({'Water_control': 2})
        elif mode == 'empircal':
            parameter_dict.update({'Water_control': 0})
            
        modified_table = []
        for i in range(len(self.default_flooding_application)):
            modified_line = self.default_flooding_application[i]
            
            for parameter_name, new_value in parameter_dict.items():
                pattern = re.compile(f'(____{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_line_align = self.custom_align(modified_line, 72)
            modified_table.append(modified_line_align)
        return modified_table
    
    # 判断
    def is_nested_dict(self, input_dict):
        if isinstance(input_dict, dict):
            for value in input_dict.values():
                if isinstance(value, dict):
                    return True
        return False
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## Mulch 子模块
class DNDCMulch:
    # 定义默认参数格式
    def __init__(self):
        self.default_mulch_none = ['____Film_applications                                                 0\n',
                                   '____Method                                                            2\n']
        
        self.default_mulch_informations = ['______Filming#                                                        1\n',
                                           '______Start_month                                                     1\n',
                                           '______Start_day                                                       1\n',
                                           '______End_month                                                       1\n',
                                           '______End_day                                                         1\n',
                                           '______Cover_fraction                                             1.0000\n',
                                           '______None                                                            0\n',
                                           '______None                                                            0\n',
                                           '______None                                                            0\n',
                                           '______None                                                            0\n',
                                           '______None                                                            0\n']
        
        self.default_parameters = {1: {'Start_month': 1,
                                       'Start_day': 0,
                                       'End_month': 1,
                                       'End_day': 1,
                                       'Cover_fraction': 1}
                                                    }
    
    # 获取默认参数的函数
    def get_default_parameters(self):
        return self.default_parameters
    
    # 定义覆膜操作
    def process_mulch(self, mode, parameter_dict=None):
        if mode == 'none':
            return self.default_mulch_none
        elif mode in ['greenhouse', 'mulch']:
            return self.process_mulch_others(mode, parameter_dict)
        else:
            raise ValueError("Invalid flooding mode")

    # 定义其他覆膜操作
    def process_mulch_others(self, mode, parameter_dict):
        if parameter_dict is None:
            raise ValueError("Please provide a mulch dictionary for mulching.")
        modified_scheduled_flooding = self.set_parameters(mode, parameter_dict)
        return modified_scheduled_flooding
    
    # 定义参数修改函数
    def set_parameters(self, mode, parameter_dict):       
        modified_list = []
        times= len(parameter_dict)
        modified_mulch_application = self.default_mulch_none
        mulch_application_first = self.default_mulch_none[0]
        pattern_first = re.compile(r'(\d+\.?\d*)')        
        modified_mulch_application_first = pattern_first.sub(str(times),  mulch_application_first)
        modified_mulch_application[0] = modified_mulch_application_first
        
        if mode == 'greenhouse':
            method = 0
        elif mode == 'mulch':
            method = 1
        mulch_application_method = self.default_mulch_none[1]
        pattern_method = re.compile(r'(\d+\.?\d*)')        
        modified_mulch_application_method = pattern_method.sub(str(method),  mulch_application_method)
        modified_mulch_application[1] = modified_mulch_application_method
        
        for mulch_times, sub_parameters_dict in parameter_dict.items():
            if not sub_parameters_dict['Cover_fraction'] in [0, 1]:
                raise ValueError("Alter cover fraction must be 0 or 1.")
            
            first_string = self.default_mulch_informations[0]
            pattern = re.compile(r'(\d+)')
            result = pattern.sub(str(mulch_times), first_string, count=1)
            modified_table = self.modify(self.default_mulch_informations[1:], sub_parameters_dict)
            modified_list.extend([result] + modified_table)
        # 将字符串设置为两端对齐，中间空格填充    
        modified_output = []
        for substr in modified_list:
            modified_output.append(self.custom_align(substr, 72))    
        return modified_output
    
    # 定义子参数修改函数        
    def modify(self, table, sub_parameter_dict):
        modified_table = []
        for i in range(len(table)):
            modified_line = table[i]
            for parameter_name, new_value in sub_parameter_dict.items():
                pattern = re.compile(f'(______{parameter_name}\\s+)([\\d\\.]+)')
                match = pattern.match(modified_line)
                if match:
                    current_value = match.group(2)
                    modified_line = modified_line.replace(current_value, str(new_value))
            modified_table.append(modified_line)
        return modified_table
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
## GrazingCut 子模块
class DNDCGrazingCut:
    def __init__(self):
        self.default = ['____Grazing_applications                                              0\n',
                        '----------------------------------------\n',
                        '____Cut_applications                                                  0\n']
    def process_grazingcut(self):
        return self.default

# Cropping 耕作整合模块
class DNDCCropping:
    def __init__(self):
        self.defaut_crop_data = ['Crop_data\n',
                                '\n',
                                'Cropping_systems                                                      1\n',
                                '\n']
        
        self.default_crop_system = ['__Cropping_system                                                     1\n',
                                    '__Total_years                                                         1\n',
                                    '__Years_of_a_cycle                                                    1\n']
        
        self.default_year = ['\n',
                            '____Year                                                              1\n']
    
    def define_practices(self, total_year, number_cropping_system, last_year_each_system, cycle_year_each_system):
        self.total_year = total_year
        self.number_cropping_system = number_cropping_system
        self.last_year_each_system = last_year_each_system
        self.cycle_year_each_system = cycle_year_each_system
    
    def cropping(self, crop, tillage, fertilzation, manure, irrigation, flooding, mulch, grazingcut):
        crop_data = self.update_cropping_data(self.defaut_crop_data, self.number_cropping_system)
        crop_systems = self.update_cropping_system(self.number_cropping_system, self.last_year_each_system, self.cycle_year_each_system)
        cropping_system = []
        cropping_system_i = []
        interel = ['----------------------------------------\n']
        for i, sub_system in crop_systems.items():
            year = self.cycle_year_each_system[i-1]
            if year == 1:
                year_data = self.default_year
                cropping_system_i = sub_system + year_data + crop[i-1] + interel + tillage[i-1] + interel +\
                    fertilzation[i-1] + interel + manure[i-1] + interel + mulch[i-1] + interel + flooding[i-1] + interel + irrigation[i-1] + interel +  grazingcut[i-1]
            if year != 1:
                for j in range(year):
                    year_data_j = self.update_year_data(j+1)
                    cropping_system_i_j = year_data_j + crop[i-1][j] + interel + tillage[i-1][j] + interel + fertilzation[i-1][j] +\
                        interel + manure[i-1][j] + interel + mulch[i-1][j] + interel + flooding[i-1][j] + interel + irrigation[i-1][j] + interel + grazingcut[i-1][j]
                    cropping_system_i.extend(cropping_system_i_j + ['\n'])
                cropping_system_i = sub_system + cropping_system_i                
            cropping_system.extend(cropping_system_i + ['\n'])
        cropping_list = crop_data + cropping_system
        # 将字符串设置为两端对齐，中间空格填充    
        cropping_output = []
        for substr in cropping_list:
            cropping_output.append(self.custom_align(substr, 72))    
        return cropping_output
    
      
    def update_cropping_data(self, data, number_cropping_system):       
        pattern = re.compile(f'(Cropping_systems\s+)(\d+)')
        updated_data = [pattern.sub(r'\g<1>{}'.format(number_cropping_system), line) for line in data]
        return updated_data
    
    def update_cropping_system(self, number_cropping_system, last_year_each_system, cycle_year_each_system):
        crop_systems = {}
        for i in range(1, number_cropping_system + 1):
            years = last_year_each_system[i - 1]
            years_cycle = cycle_year_each_system[i - 1]
            crop_systems[i] = ['__Cropping_system                                                     {}\n'.format(i),
                               '__Total_years                                                         {}\n'.format(years),
                               '__Years_of_a_cycle                                                    {}\n'.format(years_cycle)]
        return crop_systems
    
    def update_year_data(self, n):
        year_data = ['\n',
                    '____Year                                                              {}\n'.format(n)]
        return year_data
    
    # 定义一个用于字符串两端对齐的函数
    def custom_align(self, input_string, total_width):
        if any(char.isspace() and char != '\n' for char in input_string):
            char1, char2 = input_string.split()
            result = char1.ljust(total_width - len(char2)) + char2.rjust(len(char2)) + '\n'
        else: 
            result = input_string       
        return result
    
# 多模块整合与输出
class DNDCFixer:
    def __init__(self):
        self.title = ['DNDC_Input_Parameters\n']
        self.interel = ['----------------------------------------\n']
        
    # 定义一个将所有参数链接的函数
    def concat(self, site, weather, soil, cropping):
        # 首先判断模拟年限和气候数据能否对应
        simulated_years = self.get_number_from_list(site, '__Simulated_years')
        climate_files = self.get_number_from_list(weather, '__Climate_files')
        climate_file_mode = self.get_number_from_list(weather, '__Climate_file_mode')
        total_system_years = sum(self.get_system_years(cropping))
        if simulated_years != total_system_years:
            raise ValueError('The total simulated years did not match with total years of cropping systems !')
        if simulated_years != climate_files and climate_file_mode == 0:
            raise ImportError('The number of climate files did not match with the total simulated years !')
        if climate_file_mode == 1 and climate_files != 1:
            raise ImportError('The number of climate file must 1 when using 1 year for all year !')
                           
        self.result = self.title + self.interel + site + self.interel + weather + self.interel + soil + self.interel + cropping
    
    def get_number_from_list(self, list, string):
        for line in list:
            # Use a regex pattern to match __Simulated_years followed by digits
            match = re.match(rf'{string}\s+(\d+)', line)
        
            # Check if the match is found
            if match:
                # Extract the numeric value
                simulated_years = int(match.group(1))
        return simulated_years
    
    def get_system_years(self, list):
        total_years_values = []
        # Join the lines into a single string for easier pattern matching
        input_string = ''.join(list)
        # Use a regex pattern to find __Total_years followed by digits
        matches = re.finditer(r'__Total_years\s+(\d+)', input_string)

        # Iterate over matches and extract the numeric values
        for match in matches:
            total_years_values.append(int(match.group(1)))
        return total_years_values
    
    def to_dnd(self, output_file_path):
        output_string = ''.join(self.result)
        with open(output_file_path, 'w') as file:
            file.write(output_string)
            

# GEE获取气候数据模块
import ee
import pandas as pd
from tqdm import tqdm

class GEEWeatherData:
    def __init__(self):
        # 初始化类属性
        self.site_coordinates = None
        self.start_date = None
        self.end_date = None
        self.dataset = None
        self.select_band_names = None
        self.resolution = None
        self.latitude_column = None
        self.longitude_column = None
        self.site_name_column = None

    def set_site_coordinates(self, site_coordinates, latitude_column='纬度', longitude_column='经度', site_name_column='站点名称'):
        """
        设置站点经纬度坐标
        Args:
            site_coordinates (pd.DataFrame): 包含站点经纬度的 DataFrame，每个站点是一个行，包含经纬度和站点名称列。
            latitude_column (str): 包含纬度信息的列名，默认为 '纬度'。
            longitude_column (str): 包含经度信息的列名，默认为 '经度'。
            site_name_column (str): 包含站点名称信息的列名，默认为 '站点名称'。

        Returns:
            None
        """
        self.site_coordinates = site_coordinates
        self.latitude_column = latitude_column
        self.longitude_column = longitude_column
        self.site_name_column = site_name_column

    def set_time_range(self, start_date, end_date):
        """
        设置时间范围
        Args:
            start_date (str): 开始日期，格式为 'YYYY-MM-DD'
            end_date (str): 结束日期，格式为 'YYYY-MM-DD'

        Returns:
            None
        """
        self.start_date = start_date
        self.end_date = end_date

    def set_dataset(self, dataset, select_band_names):
        """
        设置数据集和波段名称
        Args:
            dataset (str): Earth Engine 数据集的 ID。
            select_band_names (list): 包含要选择的波段名称的列表。

        Returns:
            None
        """
        self.dataset = ee.ImageCollection(dataset)
        self.select_band_names = select_band_names

    def set_resolution(self, resolution):
        """
        设置分辨率
        Args:
            resolution (int): 分辨率参数。

        Returns:
            None
        """
        self.resolution = resolution

    def get_weather_data(self, time_segments=None):
        """
        获取每个站点经纬度下的逐日最高温、最低温、降水量数据
        Returns:
            dict: 包含每个站点数据的字典，键是站点名称，值是包含温度和降水数据的 Pandas DataFrame。
        """
        if any(v is None for v in [self.site_coordinates, self.start_date, self.end_date, self.dataset,
                                   self.select_band_names, self.resolution]):
            raise ValueError("请设置站点坐标、时间范围、数据集、波段名称和分辨率。")
        weather_data_dict = {}
        
        try:
            if isinstance(self.site_coordinates, pd.Series):
                self.site_coordinates = pd.DataFrame(self.site_coordinates).T

            for index, row in tqdm(self.site_coordinates.iterrows(), desc='Processing Sites', total=len(self.site_coordinates)):
                site_name = row[self.site_name_column]
                latitude = row[self.latitude_column]
                longitude = row[self.longitude_column]

                site_point = ee.Geometry.Point(longitude, latitude)
                date_range = ee.DateRange(self.start_date, self.end_date)

                # 获取数据集
                selected_dataset = self.dataset.filterBounds(site_point).filterDate(date_range)

                # 选择感兴趣的数据集属性
                selected_bands = selected_dataset.select(self.select_band_names)

                # 获取数据
                selected_data = selected_bands.getRegion(site_point, self.resolution).getInfo()
                # 将数据转换为 Pandas DataFrame
                data_df = pd.DataFrame(selected_data[1:], columns=selected_data[0])

                # 存储数据到字典
                if site_name not in weather_data_dict:
                    weather_data_dict[site_name] = {'values': data_df}
                else:
                    # 如果站点已存在，将新数据追加到原有数据
                    weather_data_dict[site_name]['values'] = pd.concat([weather_data_dict[site_name]['values'], data_df])

        except ee.EEException as e:
            print(f"Error: {e}")

            if time_segments is not None:
                print("Trying to fetch data in segments...")
                # 如果出现错误且提供了时间段，尝试按时间段获取数据
                weather_data_dict = self.get_weather_data_in_segments(time_segments)
                
        return weather_data_dict
                

    def get_weather_data_in_segments(self, time_segments):
        """
        分时间段获取数据

        Args:
            time_segments (list): 包含时间段的列表，每个时间段是一个包含开始和结束日期的元组 (start_date, end_date)。

        Returns:
            dict: 包含每个站点数据的字典，键是站点名称，值是包含温度和降水数据的 Pandas DataFrame。
        """
        weather_data_dict = {}

        for time_segment in time_segments:
            start_date, end_date = time_segment
            
            for index, row in self.site_coordinates.iterrows():
                site_name = row[self.site_name_column]
                latitude = row[self.latitude_column]
                longitude = row[self.longitude_column]

                site_point = ee.Geometry.Point(longitude, latitude)
                date_range = ee.DateRange(start_date, end_date)

                # 获取数据集
                selected_dataset = self.dataset.filterBounds(site_point).filterDate(date_range)

                # 选择感兴趣的数据集属性
                selected_bands = selected_dataset.select(self.select_band_names)

                try:
                    # 获取数据
                    selected_data = selected_bands.getRegion(site_point, self.resolution).getInfo()
                    # 将数据转换为 Pandas DataFrame
                    data_df = pd.DataFrame(selected_data[1:], columns=selected_data[0])

                    # 存储数据到字典
                    if site_name not in weather_data_dict:
                        weather_data_dict[site_name] = {'values': data_df}
                    else:
                        # 如果站点已存在，将新数据追加到原有数据
                        weather_data_dict[site_name]['values'] = pd.concat([weather_data_dict[site_name]['values'], data_df])

                except ee.EEException as e:
                    print(f"Error for site {site_name}: {e}")

        return weather_data_dict
    
# 经纬度格式转换
# 将度分秒格式转化为度格式
import pandas as pd

class DmsToDegreesConverter:
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def dms_to_degrees(self, row, col_name):
        degrees = float(row[col_name+'_degrees'])
        minutes = float(row[col_name+'_minutes'])
        seconds = float(row[col_name+'_seconds'])

        # 考虑方向
        if row[col_name+'_direction'] in ['S', 'W']:
            degrees *= -1

        return degrees + minutes/60 + seconds/3600

    def convert_dms_to_degrees(self, col_names):
        for col in col_names:
            # 使用正则表达式提取度、分、秒和方向信息
            pattern = r'(\d+)°(\d+)?[′\']?(\d+)?[″\"]?(\w)?'
            dms_data = self.df[col].str.extract(pattern)

            # 将提取的度、分、秒转换为数值型
            self.df[col+'_degrees'] = pd.to_numeric(dms_data[0], errors='coerce')
            self.df[col+'_minutes'] = pd.to_numeric(dms_data[1], errors='coerce').fillna(0)
            self.df[col+'_seconds'] = pd.to_numeric(dms_data[2], errors='coerce').fillna(0)
            self.df[col+'_direction'] = dms_data[3]

            # 应用转换函数
            self.df[col+'_degrees'] = self.df.apply(lambda row: self.dms_to_degrees(row, col), axis=1)

            # 删除不再需要的中间列
            self.df = self.df.drop(columns=[col+'_minutes', col+'_seconds', col+'_direction'])

    def get_converted_dataframe(self):
        return self.df