import pandas as pd
import numpy as np

# Create minimal data required to test the global cities functionality
data = {
    'الرقم التسلسلي': ['1', '2', '3'],
    'الجهة المسؤولة': ['جهة أ', 'جهة ب', 'جهة ج'],
    'المنطقة الادارية': ['جميع المناطق', 'الرياض', 'جميع المناطق'],
    'المدينة': ['جميع المناطق التعليمية', 'الرياض', 'جميع المدن الرئيسة بالمناطق'],
    'العنصر': ['عنصر شامل', 'عنصر محلي', 'عنصر مدن رئيسية'],
    'اسم المخرج': ['مخرج 1', 'مخرج 2', 'مخرج 3'],
    'الوصف': ['وصف شامل', 'وصف محلي', 'وصف مدن رئيسية'],
    'التاريخ': ['2023-01-01', '2023-01-02', '2023-01-03']
}

df = pd.DataFrame(data)

df.to_excel('Events_preparation.xlsx', index=False)
df.to_excel('Events_master_2.xlsx', index=False)

print("Mock files created successfully.")
