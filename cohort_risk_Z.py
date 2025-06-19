import streamlit as st
import pandas as pd
import numpy as np
import io
from io import BytesIO

st.markdown(
    "<h1 style='font-family: Arial; font-size: 36px; color: black;'>Комплексный анализ метаболитов и рисков</h1>",
    unsafe_allow_html=True)
st.markdown(
    "<h1 style='font-family: Arial; font-size: 20px; color: black;'>Загрузите необходимые файлы с данными</h1>",
    unsafe_allow_html=True)




# Функция для создания Excel файла в памяти
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=True, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return (processed_data)

# Функция для загрузки файлов
def load_file(label, key=None):
    uploaded_file = st.file_uploader(label, type=["xlsx"], key=key)
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file)
    return None

# Загрузка основных файлов
data_risks = load_file("Данные по рискам", "risks")
data = load_file("Данные исследуемой когорты", "patient")
data_controls=load_file("Референсный файл для расчета Z-score", "z-score")

metabolites=['5-hydroxytryptophan', 'ADMA',
       'Adenosin', 'Alanine', 'Antranillic acid', 'Arginine', 'Asparagine',
       'Aspartic acid', 'Betaine', 'Carnosine', 'Choline', 'Citrulline',
       'Cortisol', 'Creatinine', 'Cytidine', 'DMG', 'Glutamic acid',
       'Glutamine', 'Glycine', 'HIAA', 'Histamine', 'Histidine',
       'Homoarginine', 'Hydroxyproline', 'Indole-3-acetic acid',
       'Indole-3-butyric', 'Indole-3-carboxaldehyde', 'Indole-3-lactic acid',
       'Indole-3-propionic acid', 'Kynurenic acid', 'Kynurenine', 'Lysine',
       'Melatonin', 'Methionine', 'Methionine-Sulfoxide', 'Methylhistidine',
       'NMMA', 'Ornitine', 'Pantothenic', 'Phenylalanine', 'Proline',
       'Quinolinic acid', 'Riboflavin', 'Serine', 'Serotonin', 'Summ Leu-Ile',
       'TMAO', 'Taurine', 'Threonine', 'TotalDMA (SDMA)', 'Tryptamine',
       'Tryptophan', 'Tyrosin', 'Uridine', 'Valine', 'Xanthurenic acid', 'C0',
       'C10', 'C10-1', 'C10-2', 'C12', 'C12-1', 'C14', 'C14-1', 'C14-2',
       'C14-OH', 'C16', 'C16-1', 'C16-1-OH', 'C16-OH', 'C18', 'C18-1',
       'C18-1-OH', 'C18-2', 'C18-OH', 'C2', 'C3', 'C4', 'C5', 'C5-1', 'C5-DC',
       'C5-OH', 'C6', 'C6-DC', 'C8', 'C8-1']

def calculate_new_ratio(data, number_numinator, number_denominator, name):
    sum_numinator = 0
    for numinator in range(len(number_numinator)):
        sum_numinator += data.loc[:,number_numinator[numinator]]
    sum_denominator = 0
    for denominator in range(len(number_denominator)):
        sum_denominator += data.loc[:,number_denominator[denominator]]
    data[name] = sum_numinator / sum_denominator
    return(data)

def calculate_metabolite_ratios(data):
    data=data[['Название образца', 'Группа пациента', '5-hydroxytryptophan', 'ADMA',
       'Adenosin', 'Alanine', 'Antranillic acid', 'Arginine', 'Asparagine',
       'Aspartic acid', 'Betaine', 'Carnosine', 'Choline', 'Citrulline',
       'Cortisol', 'Creatinine', 'Cytidine', 'DMG', 'Glutamic acid',
       'Glutamine', 'Glycine', 'HIAA', 'Histamine', 'Histidine',
       'Homoarginine', 'Hydroxyproline', 'Indole-3-acetic acid',
       'Indole-3-butyric', 'Indole-3-carboxaldehyde', 'Indole-3-lactic acid',
       'Indole-3-propionic acid', 'Kynurenic acid', 'Kynurenine', 'Lysine',
       'Melatonin', 'Methionine', 'Methionine-Sulfoxide', 'Methylhistidine',
       'NMMA', 'Ornitine', 'Pantothenic', 'Phenylalanine', 'Proline',
       'Quinolinic acid', 'Riboflavin', 'Serine', 'Serotonin', 'Summ Leu-Ile',
       'TMAO', 'Taurine', 'Threonine', 'TotalDMA (SDMA)', 'Tryptamine',
       'Tryptophan', 'Tyrosin', 'Uridine', 'Valine', 'Xanthurenic acid', 'C0',
       'C10', 'C10-1', 'C10-2', 'C12', 'C12-1', 'C14', 'C14-1', 'C14-2',
       'C14-OH', 'C16', 'C16-1', 'C16-1-OH', 'C16-OH', 'C18', 'C18-1',
       'C18-1-OH', 'C18-2', 'C18-OH', 'C2', 'C3', 'C4', 'C5', 'C5-1', 'C5-DC',
       'C5-OH', 'C6', 'C6-DC', 'C8', 'C8-1']]    
    data["Arg/ADMA"]=data['Arginine']/data['ADMA']
    data['(Arg+HomoArg)/ADMA']=(data['Arginine']+data['Homoarginine'])/data['ADMA']
    data['Arg/Orn+Cit']=data['Arginine']/(data['Ornitine']+data['Citrulline'])
    data['TMAO Synthesis']=data['TMAO']/(data['Betaine']+data['C0']+data['Choline'])
    data['TMAO Synthesis (direct)']=data['TMAO']/data['Choline']
    data['Glutamine/Glutamate']=data['Glutamine']/data['Glutamic acid']
    data['Pro/Cit']=data['Proline']/data['Citrulline']
    data['HomoArg Synthesis']=data['Homoarginine']/(data['Arginine']+data['Lysine'])
    data['Kyn/Trp']=data['Kynurenine']/data['Tryptophan']
    data['Quin/HIAA']=data['Quinolinic acid']/data['HIAA']
    data['Betaine/choline']=data['Betaine']/data['Choline']
    data['C0/(C16+C18)']=data['C0']/(data['C16']+data['C18'])
    data['(C16+C18)/C2']=(data['C16']+data['C18'])/data['C2']
    data['СДК']=data['C14']+data['C14-1']+data['C14-2']+data['C14-OH']+data['C16']+data['C16-1']+data['C16-1-OH']+data['C16-OH']+data['C18']+data['C18-1']+data['C18-1-OH']+data['C18-2']+data['C18-OH']
    data['(C2+C3)/C0']=(data['C2']+data['C3'])/data['C0']
    data['C2 / C3']=data['C2']/data['C3']
    data['C4 / C2']=data['C4']/data['C2']
    data['C3 / C0']=data['C3']/data['C0']
    data['BCAA']=data['Summ Leu-Ile']+data['Valine']
    data['BCAA/AAA']=(data['Valine']+data['Summ Leu-Ile'])/(data['Phenylalanine']+data['Tyrosin'])
    data['Serotonin / Trp']=data['Serotonin']/data['Tryptophan']
    data['Phe/Tyr']=data['Phenylalanine']/data['Tyrosin']
    data['GSG_index']=data['Glutamic acid']/(data['Serine']+data['Glycine'])
    data['Glycine/Serine']=data['Glycine']/data['Serine']
    data['Tryptamine / IAA']=data['Tryptamine']/data['Indole-3-acetic acid']
    data['С2/С0']=data['C2']/data['C0']
    data['Trp/(Kyn+QA)']=data['Tryptophan']/(data['Kynurenine']+data['Quinolinic acid'])
    data['Quin/HIAA']=data['Quinolinic acid']/data['HIAA']
    data['Kynurenic acid / Kynurenine']=data['Kynurenic acid']/data['Kynurenine']
    data['Methionine + Taurine']=data['Methionine']+data['Taurine']
    data['Riboflavin / Pantothenic']=data['Riboflavin']/data['Pantothenic']
    data['Valine / Alanine']=data['Valine']/data['Alanine']
    data['ADMA / NMMA']=data['ADMA']/data['NMMA']
    data['DMG / Choline']=data['DMG']/data['Choline']
    data['Alanine / Valine']=data['Alanine']/data['Valine']
    data['Trp/Kyn']=data['Tryptophan']/data['Kynurenine']
    data['Kyn/Quin']=data['Kynurenine']/data['Quinolinic acid']
    data['Orn/Arg']=data['Ornitine']/data['Arginine']
    data['Cit/Orn']=data['Citrulline']/data['Ornitine']
    return(data)


def compute_ref_stats(data_ref):
    data_ref_std = []
    data_ref_mean = []
    metabolites = data_ref.columns[2:]
    for metabolite in metabolites:
        data_ref_std.append(data_ref[metabolite].std())
        data_ref_mean.append(data_ref[metabolite].mean())
    result_df = pd.DataFrame({
        'Metabolites': metabolites,
        'STD': data_ref_std,
        'MEANS': data_ref_mean
    })
    result_df.set_index('Metabolites', inplace=True)
    return result_df

def calculate_z_scores(data, data_ref):
    results_z_scores=pd.DataFrame({'metabolites':data.columns[2:124]})
    for index, row in data.iterrows():
        patient_zscores=[]
        for metabolite in data.columns[2:124]:
            patient_value=data.loc[index, metabolite]
            z_score=abs((patient_value-data_ref.loc[metabolite, 'MEANS'])/data_ref.loc[metabolite, 'STD'])
            patient_zscores.append(z_score)
        results_z_scores[data.loc[index, 'Название образца']]=patient_zscores
    return (results_z_scores)




selected_numinator = st.multiselect('Выберите метаболиты для числителя:', metabolites)
selected_denominator = st.multiselect('Выберите метаболиты для знаменателя:', metabolites)

name = st.text_input('Введите название нового соотношения:', 'new_ratio_1')

# Кнопка для выполнения расчета
if st.button('Рассчитать новое соотношение'):
    # Проверка, что выбраны хотя бы по одному метаболиту
    if selected_numinator and selected_denominator:
        # Вызов функции
        data_controls = calculate_new_ratio(data_controls, selected_numinator, selected_denominator, name)
        data = calculate_new_ratio(data, selected_numinator, selected_denominator, name)
        st.write('Расчет выполнен. Новое соотношение добавлено.')
    else:
        st.warning('Пожалуйста, выберите хотя бы один метаболит для числителя и знаменателя.')
if data_controls is not None:
    data_controls = calculate_metabolite_ratios(data_controls)
else:
    st.error("Пожалуйста, загрузите файл с данными по референсным образцам.")

if data is not None:
    data=calculate_metabolite_ratios(data)
else:
    st.error("Пожалуйста, загрузите файл с данными по исследуемыми образцам.")




# расчет z-scores

ref_values=compute_ref_stats(data_controls)
data_z_scores=calculate_z_scores(data, ref_values)
data_z_scores.set_index('metabolites', inplace=True)

risks = data_risks['Группа_риска'].unique()
selected_risk = st.selectbox('Выберите группу риска:', risks)

data_risks_selected=data_risks[data_risks['Группа_риска']==selected_risk]
st.write("таблица для выбранного риска:", data_risks_selected)
# Создаем таблицу с категориями
data_weights = pd.DataFrame({'Подгруппа': data_risks_selected['Категория'].unique()})

# Добавляем начальные веса (можно оставить пустыми или задать по умолчанию)
data_weights['Вес 1'] = [1.0] * len(data_weights)
data_weights['Вес 2'] = [1.0] * len(data_weights)
data_weights['Вес 3'] = [1.0] * len(data_weights)

# Используем st.data_editor для редактирования
edited_weights = st.data_editor(data_weights, num_rows="dynamic", key="weights_editor")

# После редактирования можно использовать обновленный DataFrame
st.write("Обновленная таблица весов:", edited_weights)




patients=data_z_scores.columns

i=0
for column in data_z_scores.columns:
    patient_values=[]
    for metabolite in data_risks_selected['Маркер / Соотношение'].values:
        patient_value=data_z_scores.loc[metabolite, patients[i]]
        patient_values.append(patient_value)
    data_risks_selected[patients[i]]=patient_values
    i=i+1
    
categories=data_risks_selected['Категория'].unique()
data_final=pd.DataFrame({'Пациенты':patients})
for category in categories:
    data_category=data_risks_selected[data_risks_selected['Категория']==category]
    category_means=[]
    for patient in patients:
        category_means.append(data_category[patient].mean().round(3))
    data_final[category]=category_means


# расчет среднего Z-score по всем подгруппам в риске 
data_final['Среднее по подгруппам'] = data_final[categories].mean(axis=1)

# расчет среднего Z-score по всем подгруппам в риске, умноженных на вес 1 
i=0
df_weight_1=pd.DataFrame({'Пациенты':patients})
df_weight_2=pd.DataFrame({'Пациенты':patients})
df_weight_3=pd.DataFrame({'Пациенты':patients})

for category in categories:
    df_weight_1[category]=data_final[category]*edited_weights.loc[i,'Вес 1']
    df_weight_2[category]=data_final[category]*edited_weights.loc[i,'Вес 2']
    df_weight_3[category]=data_final[category]*edited_weights.loc[i,'Вес 3']
    i=i+1

data_final['Среднее по подгруппам вес 1'] = df_weight_1[categories].mean(axis=1)
data_final['Среднее по подгруппам вес 2'] = df_weight_2[categories].mean(axis=1)
data_final['Среднее по подгруппам вес 3'] = df_weight_3[categories].mean(axis=1)    
data_final[[ 'Среднее по подгруппам','Среднее по подгруппам вес 1' ,'Среднее по подгруппам вес 2', 'Среднее по подгруппам вес 3']] = data_final[['Среднее по подгруппам','Среднее по подгруппам вес 1' ,'Среднее по подгруппам вес 2', 'Среднее по подгруппам вес 3']].round(3)

#st.write("Данные по категориям:", data_final)
if data_final is not None:
    st.write("### Результаты исследований")
    st.dataframe(data_final)
        
    excel_combined = to_excel(data_final)
    st.download_button(
        label="Скачать результат",
        data=excel_combined,
        file_name='результат.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.write("### Оценка рисков пациента")
