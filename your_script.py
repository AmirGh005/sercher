from telethon import TelegramClient, events

# اطلاعات حساب کاربری
api_id = '24447677'  # API ID خود را اینجا وارد کنید
api_hash = 'b5b1aee85d98b5e14a66d990472bd09d'  # API Hash خود را اینجا وارد کنید
phone_number = '+989362482673'

# متن خاصی که به دنبال آن هستید
TARGET_TEXTS = [
    'machine learning', 'deep learning', 'regression', 'AI', 'ماشین لرنینگ',
    'یادگیری ماشین', 'data science', 'عصبی', 'یادگیری عمیق', 'هوش مصنوعی',
    'تحلیل داده', 'علوم کامپیوتر', 'علوم داده', 'Machine learning',
    'Deep learning', 'Regression', 'ai', 'Ai', 'Data science', 'دیپ لرنینگ',
    'تحلیلگر','پایتون','برنامه نویس','ماشین','لرنینگ','زبان R','مهندس کامپیوتر',
    'کامپیوتر','زبان طبیعی','nlp','NLP','بینایی ماشین','یادگیری تقویتی','vision',
    'reinforcement','Reinforcement','الگوریتم'
]

# لیستی از آیدی کانال‌هایی که پیام‌ها باید به آنها فروارد شود
TARGET_CHANNELS = ['@Amir_Gh_0505', '@fftty10', '@iranestekhdam_ir', '@estekhdami_com', '@daneshkargroup', 
                  '@donyayeproject', '@bds_job', '@freelancer_gray', '@remote', '@outsource456', 
                  '@datasciencejobs', '@datasciencejobs', '@AiIndiaJobs', '@jobpremier', '@FreelancerH', 
                  '@BoardOutsource', '@getjobss', '@estekhdam_doorijob', '@karyabi_doorijob', '@DorkariLand', 
                  '@remotejobshg', '@freelan3ers', '@divar_daneshjooyan', '@bia2tamrin', '@datascienceml_jobs', 
                  '@D_I_V_A_R_ir', '@FreelancerEN', '@AloJobs', '@doorkaari', '@remote_vakansii', '@ProzheLancer', 
                  '@freelan3ers', '@project_board', '@bia2tamrin', '@mihan_proje', '@karyabi_dorkar', '@SevenProzhe', 
                  '@freelancer_booth', '@best_projectt', '@projeh_2400', '@karyabanproject', '@jobsearch93', '@dor_kar', 
                  '@project_panel', '@karynet', '@theProjectLand', '@ProjectsOrder', '@Proje_Yab', '@Project_R00m', 
                  '@jobfinder2021', '@workinja', '@farayand_project', '@weproje', '@Daneshjoo_Com', '@Freelancersho_ir', 
                  '@freelancer_job', '@danshjo_bartar', '@Daneshjoo_work07', '@UniJobz', '@sent_projects', 
                  '@freelanceran_tel', '@prozhe_pazhoh', '@project_bartar', '@shoghl_yaby', '@PROAJECTE', 
                  '@Project930', '@freelancer_partak', '@ful_jab', '@proaject', '@unii_kar', '@online24_24', 
                  '@UB_Projects', '@project_land_best', '@porojemehvar', '@projheh', '@Tehran_Project_1', 
                  '@projjecthal', '@AloFreelancer', '@full_jab', '@prajects', '@proojehforsat', '@iProject']

# متغیر برای شمارش تعداد فرواردها
forward_count = 0

# ایجاد یک کلاینت تلگرام
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    global forward_count  # متغیر سراسری برای شمارش فرواردها
    message_text = event.message.message
    
    if any(target_text in message_text for target_text in TARGET_TEXTS):
        for channel in TARGET_CHANNELS:
            await client.forward_messages(channel, event.message)
            forward_count += 1  # افزایش شمارنده به ازای هر فروارد

        print(f'Total forwards so far: {forward_count}')

async def main():
    # ورود به حساب کاربری
    await client.start(phone=phone_number)
    
    # شروع به مانیتور کردن پیام‌ها
    print("Listening for messages...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
