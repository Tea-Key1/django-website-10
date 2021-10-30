# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Post

# ListViewは一覧を簡単に作るためのView
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# DetailViewは詳細を簡単に作るためのView
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post
# CreateViewは新規作成画面を簡単に作るためのView
class Create(CreateView):
    model = Post
    
    # 編集対象にするフィールド
    fields = ["name", "mail"]

class Update(UpdateView):
    model = Post
    fields = ["name", "mail"]

class Delete(DeleteView):
    model = Post
    
    # 削除したあとに移動する先（トップページ）
    success_url = "/"

from django.views.generic.edit import FormView
from . import forms
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import imaplib
import email


class Sousin(FormView):
    form_class = forms.TextForm
    template_name = "index.html"
    
        # フォームの入力にエラーが無かった場合に呼ばれます
    def form_valid(self, form):
        # form.cleaned_dataにフォームの入力内容が入っています
        data = form.cleaned_data
        from_addr = data["mymail"]
        from_pass = data["mypass"]
        to_addr = data["youmail"]
        body = data["body"]
        subject = "Group10"
        
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["To"] = to_addr
        msg["From"] = from_addr
         
        # メール送信処理
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_addr, from_pass)
        server.send_message(msg)
        server.quit()
        # テンプレートに渡す
        ctxt = self.get_context_data(new_text="送信完了", form=form)
        return self.render_to_response(ctxt)

class Jusin(FormView):
    form_class = forms.Text2Form
    template_name = "index2.html"
    
            # フォームの入力にエラーが無かった場合に呼ばれます
    def form_valid(self, form):
        # form.cleaned_dataにフォームの入力内容が入っています
        data = form.cleaned_data
        UserName = data["mymail"]
        PassName = data["mypass"]
        search_option='SUBJECT "Group10"'
        fetch_num = 5
        str_A = []
        str_B = []
        i=0
        gmail = imaplib.IMAP4_SSL("imap.gmail.com", '993')
        gmail.login(UserName, PassName)
        gmail.select()
        
        head, data = gmail.search(None, search_option)
        datas=data[0].split()
        if (len(datas)-fetch_num) < 0:
            fetch_num = len(datas)
        
        for num in reversed(datas[len(datas)-fetch_num::]):
            h, d = gmail.fetch(num, '(RFC822)')
            raw_email = d[0][1]
            # 文字コード取得
            msg = email.message_from_string(raw_email.decode('utf-8'))
            msg_encoding = email.header.decode_header(msg.get('Subject'))[0][1] or 'iso-2022-jp'
            # タイトルの情報を抽出
            msg_subject = email.header.decode_header(msg.get('Subject'))[0][0]
            if msg_subject=="":
              subject="件名なし"
            elif msg_encoding=='iso-2022-jp':
              subject = msg_subject
            else:
              subject = str(msg_subject.decode(msg_encoding))
              
            # エンコーディング
            # タイトル
        
            # 差出人アドレス
            ad=email.header.decode_header(msg.get('From'))
            ms_code=ad[0][1]
            if(ms_code!=None):
              address=ad[0][0].decode(ms_code)
              address+=ad[1][0].decode(ms_code)
            else:
              address=ad[0][0]
            # 作成日時
            # date = dateutil.parser.parse(msg.get('Date')).strftime("%Y/%m/%d %H:%M:%S")
        
            #ヘッダ表示
            # print(subject)
            print("-"*25)
            print(address)

            
            # print(date)
        
            # 本文の抽出
            if msg.is_multipart() is False:
                # シングルパートのとき
                payload = msg.get_payload(decode=True) # 備考の※1
                charset = msg.get_content_charset()    # 備考の※2
                
                if charset is not None:
                    payload = payload.decode(charset, "ignore")
        
            else:
                # マルチパートのとき
                for part in msg.walk():
                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue
                    charset = part.get_content_charset()
                    if charset is not None:
                        payload = payload.decode(charset, "ignore")
                        break
            print(payload)
            print("-"*25)
            str_A = [address, payload, ('-'*(220-len(payload)))]
            str_Aa = ("-"*3).join(str_A)
            str_B.append(str_Aa)
        
        str_C = "\n------\n"
        str_Bb = "\n\n".join(str_B)
        new_text = str_Bb + str_C
        gmail.close()
        gmail.logout()
        # テンプレートに渡す
        ctxt = self.get_context_data(new_text=new_text, form=form)
        return self.render_to_response(ctxt)









