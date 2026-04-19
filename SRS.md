## Yazılım Gereksinimleri Belirtimi (SRS)

<div align="center">

# Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü

</div>

(Multi-Agent Legal Ops)

Kurum: Gazi Universitesi

Grup Ismi: Lagent

Hazirlayanlar: Mustafa Emir Ceran-24118080702 Mert Ayranci-24118080752 Osman Gazi Atalay-23118080703

Tarih: 6 Nisan 2026

Sürüm: 1.1

## Revizyon Geçmişi

<table border="1"><tr><td>Sürüm</td><td>Tarih</td><td>Açıklama</td><td>Yazar</td></tr><tr><td>1.0</td><td>15.03.2026</td><td>İlk sürüm oluşturuldu.</td><td>Lagent</td></tr><tr><td>1.1</td><td>06.04.2026</td><td>SRS şablonuna uygun olarak bölüm yapısı güncellendi. Gerekli Durum ve Modlar, Uyarlama, Emniyet, Güvenlik ve Gizlilik, Ortam, Bilgisayar Kaynak, Yazılım Kalite Faktörleri, Tasarım Kısıtlamaları, Personel, Eğitim, Lojistik, Ambalajlama ve Öncelik/Kritiklik bölümleri eklendi.</td><td>Lagent</td></tr></table>

## İçindekiler

Revizyon Geçmişi 1

1 GİRİŞ 4

1.1 Ürün Genel Bakışı 4

1.1.1 Ürün Perspektifi 4

1.1.2 Ürün İşlevleri 5

1.1.3 Kullanıcı Sınifları ve Özellikleri 6

1.1.4 Çalışma Ortamı 6

1.1.5 Tasarım ve Uygulama Kısıtları 6

1.1.6 Varsayımlar ve Bağımlılıklar 7

2 GEREKSİNİMLER 8

2.1 Gerekli Durum ve Modlar 8

2.2 YKE Fonksiyonel Gereksinimleri 8

2.2.1 Kullanıcı Kayıt ve Kimlik Doğrulama 8

2.2.2 Sözleşme Yükleme ve Doküman İşleme 9

2.2.3 Madde Ayrıştırma ve Sıniflandırma 9

2.2.4 Politika Kontrolü ve Risk Değerlendirmesi 9

2.2.5 Revizyon Önerisi ve Karşılastırmalı Görünüm 10

2.2.6 Onay Akışı 10

2.2.7 Raporlama 11

2.2.8 Playbook Yönetimi 11

2.3 YKE Dış Arayüz Gereksinimleri 11

2.3.1 Arayüz Tanımlaması ve Diyagramları 11

2.3.2 Kullanıcı Arayüzü (UI-01) 12

2.3.3 LLM Servisi Arayüzü 13

2.3.4 Veritabanı Arayüzü 13

2.3.5 Vektör Arama Arayüzü 14

2.3.6 Önbellek Arayüzü 14

2.3.7 Nesne Depolama Arayüzü 14

2.3.8 İletişim Yöntemleri 14

2.4 YKE Dahili Arayüz Gereksinimleri 14

2.5 YKE Dahili Veri Gereksinimleri 15

    2.5.1 İlişkisel Veritabanı 15

    2.5.2 Vektör Veritabanı 16

    2.5.3 Önbellek ve Durum Yönetimi 16

    2.5.4 Dosya Depolama 16

2.6 Uyarlama Gereksinimleri 16

2.7 Emniyet Gereksinimleri 17

2.8 Güvenlik ve Gizlilik Gereksinimleri 17

2.9 YKE Ortam Gereksinimleri 18

2.10 Bilgisayar Kaynak Gereksinimleri 18

    2.10.1 Bilgisayar Donanım Gereksinimleri 18

    2.10.2 Bilgisayar Donanımı Kaynak Kullanımı Gereksinimleri 18

    2.10.3 Bilgisayar Yazılım Gereksinimleri 18

    2.10.4 Bilgisayar İletişim Gereksinimleri 19

2.11 Yazılım Kalite Faktörleri 19

2.12 Tasarım ve Uygulama Kısıtlamaları 20

2.13 Personelle İlgili Gereksinimler 20

2.14 Eğitimle İlgili Gereksinimler 21

2.15 Lojistikle İlgili Gereksinimler 21

2.16 Diğer Gereksinimler 21

2.17 Ambalajlama Gereksinimleri 21

2.18 Gereksinimlerin Önceliği ve Kritikliği 22

# 3 EK MATERYALLER 23

3.1 Kullanım Senaryoları Özeti 23

    3.1.1 Genel Kullanım Senaryosu Diyagramı 23

    3.1.2 Kullanım Senaryoları Tablosu 23

    3.1.3 Kullanım Senaryosu Diyagramları 24

3.2 Veri Akışı Genel Görünümü 37

    3.2.1 UML Sınif Diyagramı 37

    3.2.2 Veri Akışı 37

3.3 Sözlük 37

## 1 GIRIS

Bu Yazılım Gereksinimleri Belirtimi (SRS) dokümanı, Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü (Multi-Agent Legal Ops) sisteminin işlevsel ve işlevsel olmayan gereksinimlerini kapsamlı biçimde tanımlamaktadır.

Dokümanın hedef kitlesi; yazılım geliştiriciler, test mühendisleri, proje yöneticileri, hukuki danışmanlar ve diğer paydaşlardır. Bu belge, sistemin ne yapması gerektiğini ortaya koyar; nasıl yapilacağına ilişkin tasarım kararları SDD (Software Design Document) kapsamında ele alınacaktır.

Günümüzde bireyler ve küçük-orta ölçekli işletmeler, kira sözleşmelerinden ticari anlaşmalara kadar geniş bir yelpazede hukuki metinlerle karşılasmaktadır. Bu metinlerin doğru anlaşılması, risklerin zamanında tespit edilmesi ve gerektiğinde müzakere süreçlerinin yürütülmesi genellikle uzmanlık gerektiren, zaman alıcı ve maliyetli bir süreçtir. Mevcut durumda kullanıcılar çoğunlukla her sözleşme için ayrı avukat desteği almak zorunda kalmakta, bu da özellikle sıradan bireyler ve küçük işletmeler için erişilebilirlik sorunu yaratmaktadır.

Bu proje, söz konusu boşluğu doldurmak amacıyla çok ajanlı (multi-agent) bir yapay zeka asistanı geliştirmeyi hedeflemektedir. Sistem; sözleşme metinlerini otomatik olarak ayrıştıracak, madde bazında sınıflandıracak, kullanıcının belirlediği politikalara göre risk analizi yapacak, riskli maddeler için alternatif ifade önerileri sunacak ve tüm bu süreçleri bütünleşik bir onay akışı icinde yönetecektir.

Projenin temel motivasyonu, hukuki inceleme süreçlerinin demokratikleştirilmesi ve yapay zeka destekli otomasyon sayesinde hem zaman hem de maliyet tasarrufu sağlanmasidır. Sistem, avukat desteğinin tamamen yerine geçmeyi değil; ön inceleme, risk tespiti ve müzakere hazirlığı aşamalarında kullanıcıya güvenilir bir asistanlık sunmayı amaçlamaktadır.

## 1.1 Ürün Genel Bakışı

## 1.1.1 Ürün Perspektifi

Çok Ajanlı Sözleşme İnceleme ve Müzakere Orkestratörü, bağımsız (stand-alone) bir web uygulaması olarak geliştirilecektir. Sistem herhangi bir mevcut kurumsal yazılımın parçası veya uzantısı değilir.

Sistem, birbiriyle koordineli çalışan birden fazla yapay zeka ajanindan oluşan çok katmanlı bir mimari üzerine inşa edilecektir. Bu katmanlar genel hatlarıyla şöyledir:

1. Doküman İşleme Katmani: Kullanıcıının yüklediği sözleşme dosyalarının (PDF, DOCX vb.) düz metne dönüştürülmesi; taranmış belgeler için optik karakter tanıma (OCR) desteği sunulması.

2. Çok Ajanlı Yapay Zeka Katmanı: Madde ayrıştırma, sınıflandırma, risk değerlendirme ve revizyon önerisi gibi görevlerin, her biri belirli bir sorumluluk alanına sahip bağımsız ajanlar tarafından yürütülmesi; bu ajanların bir orkestrasyon mekanizması aracılığıyla koordineli çalışması.

3. Bilgi Erişim Katmanı (RAG): Kullanıcınin tanımladığı politikalar (Playbook) ve referans madde havuzunun vektörel olarak indekslenmesi; analiz sırasında anlamsal benzerlik aramasıyla bağlam zenginleştirme yapılması.

4. Sunucu Tarafi API Katmani: İstemci uygulaması ile arka plan servisleri arasındaki iletişimi sağlayan, RESTful prensiplere uygun uygulama programlama arayüzü.

5. İstemci Katmani: Kullanıcıların sisteme eriştiği, sözleşme yükleyip analiz sonuçların incelediği, kararların verdigi modern web tabanlı arayüz.

6. Veri Yönetimi Katmanı: İlişkisel veritabanı , vektör veritabanı , önbellek mekanizması ve nesne depolama bileşenlerinin bütünleşik yönetimi.

## 1.1.2 Ürün İşlevleri

Sistemin sunacağı başlıca işlevler aşağıda özetlenmiştir:

- Sözleşme Yükleme ve Metin Dönüştürme: Kullanıcıların farklı formatlardaki sözleşme dosyalarını sisteme yüklemesi; bu dosyaların otomatik olarak işlenebilir düz metne dönüştürülmesi.

- Madde Bazlı Ayrıştırma: Sözleşme metninin yapısal olarak ayrı maddelere bölünmesi ve her maddenin bağımsız bir birim olarak ele alınması.

- Otomatik Sınıflandırma: Ayrıstırılan her maddenin, önceden tanımlanmış hukuki kategorilere (gizlilik, tazminat, fesih, fikri mülkiyet, sorumluluk sınırlandırma, uyuşmazlık çözümü, ödeme koşullari vb.) yapay zeka destekli olarak atanması.

- Politika Uyumluluk Kontrolü: Her maddenin, kullanıcıının tanımladığı Playbook kurallarına göre uyumluluk açısından değerlendirilmesi; eksik veya çelişkili hükümlerin otomatik tespit edilmesi.

- Risk Değerlendirmesi: Maddelerin ticari ve hukuki boyutlarıyla birlikte çok seviyeli bir risk skalasında (düşük, orta, yüksek) derecelendirilmesi.

- Revizyon Önerisi Üretimi: Riskli bulunan maddeler için, kullanıcı politikalari ve referans madde havuzu temelinde alternatif ifade önerilerinin otomatik olarak üretilmesi.

- Karşılastırmalı Görünüm (Redline): Orijinal madde metni ile önerilen revizyon metninin, ekleme ve silme farklarının görsel olarak vurgulandığı karşılastırmalı bir biçimde sunulması.

- Onay Akışı Yönetimi: Her madde için ayrı ayrı onay, red veya yeniden revize kararı verilebilmesi; bu kararların durum geçişleriyle (taslak, incelemede, onaylandı, reddedildi) izlenebilmesi.

- Denetim İzi (Audit Trail): Kullanıcıların verdiği tüm kararların, yorumların ve işlem zaman damgalarının kayıt altına alınması.

- Raporlama ve Dısa Aktarım: İnceleme sonuçlarının özet ve detaylı rapor olarak görüntülenmesi; raporların ve revize edilmiş sözleşme taslağının dosya olarak indirilebilmesi.

- Playbook Yönetimi: Kullanıcıların kendi sözleşme politikalarını (kabul edilebilir ifadeler, reddedilecek ifadeler, eşik değerler) tanımlayabilmesi, düzenleyebilmesi ve bu kuralların analiz sürecine yansıtılması.

## 1.1.3 Kullanıcı Sınıfları ve Özellikleri

Sistemin hedef kullanıcı kitleleri aşağıdaki gibi sınıflandırılmaktadır:

<table border="1"><tr><td>Kullanıcı Tipi</td><td>Profil</td><td>Teknik Yeterlilik</td></tr><tr><td>Bireysel Kullanıcı</td><td>Kira, iş veya hizmet sözleşmelerini inceleyen bireyler.Hukuki terminolojiye aşinalıkları sınırlidır.</td><td>Temel bilgisayar ve internet kullanımı.Hukuki ön bilgi gerektirmez.</td></tr><tr><td>KOBİ Yöneticisi</td><td>Ticari sözleşmeleri,tedarikci anlaşmalarını ve ortaklık protokollerini inceleyen küçükorta ölçekli işletme sahipleri veya yöneticileri.</td><td>Orta düzey bilgisayar kullanımı.Temel ticari sözleşme bilgisi.</td></tr><tr><td>Hukuk Danışmanı</td><td>Sözleşme inceleme sürecini hızlandırmak,ön tarama ve risk analizini otomatikleştirmek isteyen avukatlar ve hukuk müsavirleri.</td><td>İleri düzey hukku bilgi, orta düzey teknik yeterlilik.</td></tr><tr><td>Sistem Yöneticisi</td><td>Platformun kurulum,yapılandırması,kullanımı yönetimi ve bakım süreçlerini yürütent teknik personel.</td><td>İleri düzey teknik yeterlilik.Sunucu yönetimi ve veritabanı bilgisi.</td></tr></table>

## 1.1.4 Çalısma Ortamı

Sistem bir web uygulaması olarak çalışacaktır. Kullanıcılar, modern bir web tarayıcısi araçılığıyla herhangi bir ek yazılım kurulumu gerektirmeden sisteme erişebilecektir. Sunucu tarafı bileşenleri konteynerize edilerek farklı altyapı ortamlarında çalıştırılabilecektir.

## 1.1.5 Tasarım ve Uygulama Kısıtları

- Sistem, doğal dil işleme ve metin üretimi görevlerinde harici bir büyük dil modeli (LLM) servisine bağımlidır. Bu servisin erişilebilirliği ve yanıt kalitesi, sistem performansını doğrudan etkiler.

- Optik karakter tanıma (OCR) doğruluğu, yüklenen taranmış dokümanların görüntü kalitesine bağlıdır; düşük çözünürlüklü veya bozuk taramalar hatalı metin çıktısına yol açabilir.

- Sistem, hukuki tavsiye niteliği taşımaz ve bir avukatın yerini almayı hedeflemez. Nihai karar ve sorumluluk her zaman kullanıcıya aittir.

- İlk sürümde yalnızca Türkçe sözleşme metinleri desteklenecktir.

- Yüksek risk seviyesindeki maddelerde otomatik onay mekanizması uygulanmayacak; bu maddelerde insan onayı zorunlu olacaktır.

- Yapay zeka modelinin ürettiği tüm çıktılar (sınıflandırma, risk skoru, revizyon önerisi), deterministik olmayan doğası geregi yanlış pozitif veya yanlış negatif sonuclar içerebilir; bu nedenle çapraz doğrulama mekanizmaları uygulanacaktır.

## 1.1.6 Varsayımlar ve Bağımlılıklar

- Kullanıcıların güncel bir web tarayıcısına ve stabil bir internet bağlantısına sahip olduğu varsayilmaktadır.

- Harici dil modeli servisinin kesintisiz ve kabul edilebilir geçikme süreleriyle erişilebilir olduğu varsayilmaktadir.

- Kullanıcıların sisteme yükleyeceği sözleşme dosyalarının makine tarafından okunabilir kalitede olduğu varsayilmaktadir.

- Sunucu tarafı altyapı bileşenlerinin (veritabanı, önbellek, dosya depolama) konteyner ortamında çalıştırılacağı varsayilmaktadır.

- Kullanıcıların Playbook oluşturken temel sözleşme terminolojisine aşina olduğu varsayılmaktadır, sistem yorumlayıcı katman içerdiği için Playbook girdisi kapsayıcı ve konuyla alakalı olmalidir.

## 2 GEREKSİNİMLER

## 2.1 Gerekli Durum ve Modlar

Sistem aşağıdaki çalışma durumlarma sahip olacaktır:

Boşta (Idle) Kullanıcı oturum açmış ancak herhangi bir analiz işlemi başlatmamıştır. Sistem, yeni görev bekleme durumundadır; kullanıcı dashboard’u görüntüleyebilir, sözleşme listesine göz atabilir veya Playbook yönetimi yapabilir.

Aktif – Analiz İşlemi Kullanıcı bir sözleşme yüklemiş ve otomatik analiz süreci başlamıştır. Bu durumda ayrıştırma, sınıflandırma, risk değerlendirme ve revizyon önerisi ajanları sıralı/paralel olarak çalışmaktadır. Kullanıcıya gerçek zamanlı ilerleme bildirimi gönderilir.

Aktif – İnceleme ve Karar Analiz tamamlanmış, kullanıcı madde bazlı sonuçları incelemekte ve onay/red kararlarını vermektedir. Bu modda yapay zeka ajanları pasiftir; kullanıcı etkileşimi ön plandadır.

Bozulmuş (Degraded) Harici dil modeli (LLM) servisi veya bir altyapı bileşeni (veritabanı, önbellek vb.) erişilemez durumdadır. Sistem, daha önce tamamlanmış analiz sonuçlarına erişimi sürdürür ancak yeni analiz başlatılamaz. Kullanıcıya uygun hata mesajı gösterilir.

Bakım (Maintenance) Planlı bakım süresinde sistem geçici olarak kullanım kapatılır.

Kullanıcılara bakım bildirimi gösterilir.

Her gereksinim, ilgili durum ve modlarla ilişkilidir. Fonksiyonel gereksinimler ağırlıkli olarak Aktif - Analiz İşlemi ve Aktif - İnceleme ve Karar durumlarıyla; güvenilirlik ve hata yönetimi gereksinimleri Bozulmuş durumuyla ilişkilidir.

## 2.2 YKE Fonksiyonel Gereksinimleri

Bu bölüm, sistemin her bir fonksiyonel alanı ile ilişkili gereksinimleri ayrintılandırmak üzere alt paragraflara bölünmüştür.

## 2.2.1 Kullanıcı Kayıt ve Kimlik Doğrulama

1. Sistem, kullanıcıların e-posta adresi ve şifre ile yeni hesap oluşturmasına izin verecektir.

2. Sistem, token tabanlı bir kimlik doğrulama mekanizması kullanacaktır.

3. Başarısız giriş denemelerinde kullanıcıya en fazla 2 saniye içinde hata mesajları gösterilecektir.

## 2.2.2 Sözleşme Yükleme ve Doküman İşleme

1. Sistem, (PDF, DOCX) formatlarını kabul edecektir.

2. Yüklenen dosya boyutu, yapılandırılabilir bir üst limite (varsayılan 10 MB) tabi olacaktır.

3. Sistem, yüklenen dokümanları otomatik olarak düz metne dönüştürecektir.

4. Taranmış (görüntü tabanlı) belgelerde metin çıkarımı için optik karakter tanıma (OCR) uygulanacaktır. 10 MB büyükklüğundeki bir PDF maksimum 30 saniye içinde düz metne dönüştürülecektir.

5. Dönüştürme işlemi başarısız olduğunda kullanıcıya nedenini açıklayan anlamlı bir hata mesajı gösterilecektir.

6. Yüklenen orijinal dosyalar, nesne depolama servisi üzerinde güvenli biçimde saklanacaktır.

## 2.2.3 Madde Ayrıştırma ve Sınıflandırma

1. Ayrıştırma ajanı (Clause Agent), dönüştürülmüş metni sözleşme maddelerine böllecektir.

2. Her madde; gizlilik, tazminat, fesih, fikri mülkiyet, sorumluluk sınırlandırma, uyuşmazlık çözümü, ödeme koşulları ve genel hükümler gibi önceden tanımlanmış kategorilere sıniflandırılacaktır.

3. Sınıflandırma sonuçları, yapılandırılmış veri formatında döndürülecektir.

4. Sistem, her madde için siniflandırma güven skorunu (confidence score) hesaplaya-caktır.

5. Güven skoru belirlenen eşiğin altında kalan maddeler “Belirsiz” olarak işaretlenecek ve kullanıcıın manuel doğrulamasına sunulacaktır.

6. 10 sayfalık standart bir sözleşmenin maddelere ayrıştırılması ve sınıflandırılması 120 saniye içinde tamamlanacaktır. (Yanıt süresi LLM servisine göre değişkenlik gösterebilir.) Sınıflandırma doğruluğu en az %70 olacaktır.

## 2.2.4 Politika Kontrolü ve Risk Değerlendirmesi

1. Risk değerlendirme ajanı (Risk Agent), sınıflandırılmış maddeleri kullanıcının Playbook'undaki kurallarla karşılastıracaktır.

2. Karşılastırma işlemi, anlamsal benzerlik araması (RAG altyapısı) kullanilarak gerçekleştirilecektir.

3. Her maddeye düşük, orta ve yüksek olmak üzere üç seviyeli bir risk derecesi atanacaktır.

4. Risk değerlendirmesi, hem ticari hem de hukuki boyutları kapsayan çok boyutlu bir rubriğe dayandırılacaktır.

5. Playbook'ta tanımlanan ancak sözleşmede yer almayan hükümler otomatik olarak tespit edilecek ve raporlanacaktır.

6. Yapay zeka modelinin ürettiği risk değerlendirmeleri, deterministik kural mekanizmalariyla çapraz doğrulanacaktır.

7. Risk değerlendirme sonuçlarında her madde için riskin gerekçesi açıklama olarak sunulacaktır.

8. Bir sözleşmenin tüm maddeleri için risk değerlendirmesi 120 saniye içinde tamam-lanacaktır. (Yanıt süresi LLM servisine göre değişkenlik gösterebilir.)

## 2.2.5 Revizyon Önerisi ve Karşılastırmalı Görünüm

1. Sistem, yüksek ve kritik risk seviyesindeki maddeler için otomatik olarak en az 1 alternatif ifade öneri üretecektir. Öneri üretimi maksimum 5 saniye icinde tamamlanacaktır.

2. Öneri üretiminde kullanıcı Playbook'u baglam olarak kullanılacaktır.

3. Orijinal ve önerilen metinler arasındaki farklar, karşılasştırmalı (redline/diff) formatta görüntülenecektir.

4. Kullanıcı, sistem tarafından önerilen revizyon metnini doğrudan arayüz üzerinden düzenleyebilecektir.

5. Gerektiğinde revize edilmiş sözleşmenin doküman formatında dışa aktarılması saglanacaktır.

## 2.2.6 Onay Akışı

1. Onay akışı, durum makinesi mantığıyla yönetilecektir. Temel durum geçişleri: Taslak Oluşturuldu → İncelemede → Onay Bekliyor → Onaylandı / Reddedildi.

2. Her madde için bağmışiz olarak onay, red veya yeniden revize kararı verilebilecektir. Kullanıcı bir madde için karar verdikten sonra sistem bu kararı maksimum 1 saniye icinde kaydedecektir. Audit log kayıtlar %100 doğrulukla saklanacaktır.

3. Yüksek risk seviyesindeki maddelerde otomatik onay yapılmayacak; insan onayı zorunlu olacaktır.

4. Tüm onay ve red kararları; karar veren kullanıcı bilgisi, zaman damgası ve varsa yorum ile birlikte denetim izi (audit trail) olarak kaydedilecektir.

5. Reddedilen veya revize edilen maddeler, güncellenmiş öneriyle birlikte yeniden değerlendirme döngüsüne alınabilecektir.

## 2.2.7 Raporlama

1. Sistem, sözleşme inceleme sonuçlarım özet rapor olarak gösterecektir. Özet raporda toplam madde sayısı, risk seviyesi dağılımı ve karar durumlar yer alacaktır.

2. Detaylı rapor, her madde için kategori, risk seviyesi, risk gerekçesi, verilen karar ve kullanıcı yorumu bilgilerini içerecektir.

3. Raporlar, PDF ve DOCX formatlarında indirilebilecektir.

## 2.2.8 Playbook Yönetimi

1. Kullanıcı, kendi sözleşme politikalarını (Playbook) oluşturabilecek, düzenleyebilecek ve silebilecektir.

2. Playbook kuralları; kabul edilebilir ifadeler, reddedilecek ifadeler, zorunlu olması gereken hükümler ve sayısal eşik değerler olarak yapılandırılabilecektir.

3. Playbook güncellendiğinde, ilgili vektörel indeksler otomatik olarak yenilenecektir.

4. Kullanıcı, birden fazla Playbook tanımlayabilecek ve sözleşme analizinde hangi Playbook'un kullanılacağını seçebilecektir.

5. Sistem, varsayılan bir Playbook şablonu sunacaktır; kullanıcılar bu şablonu temel alarak kendi kurallarını oluşturabilecektir.

## 2.3 YKE Dış Arayüz Gereksinimleri

Bu bölüm, sistemin harici arayüzleri (kullanıcılar, harici servisler ve diğer sistemlerle veri bölüşme, saglama veya değiştirme gerektiren ilişkiler) için gereksinimleri belirtir.

## 2.3.1 Arayüz Tanımlaması ve Diyagramları

Sistemin harici arayüzleri aşağıda tanımlanmaktadır:

<table border="1"><tr><td>Arayüz Elemanı</td><td>Tip</td><td>Açıklama</td></tr><tr><td>Web Kullanıcı Ara-yüzü</td><td>Kullanıcı-Sistem</td><td>Kullanıcıların tüm sistem işlevlerine eriştiği web tabanlı ön yüz ara-yüzü.</td></tr><tr><td>LLM API Ara-yüzü</td><td>Sistem-Sistem</td><td>Yapay zeka görevleri (sıniflandırma,risk analizi, revizyon) için harici büyük dil modeli servisine yapılan API çağrıları.</td></tr><tr><td>RESTful API</td><td>İstemci-Sunucu</td><td>İstemci uygulaması ile sunucu ta-rafı servisleri arasındaki yapılandırılmış veri iletişimi.</td></tr><tr><td>WebSocket Ara-yüzü</td><td>Sunucu-İstemci</td><td>Uzun süren işlemlerde gerçek zamanlı ilerleme bildirimi.</td></tr></table>

## 2.3.2 Kullanıcı Arayüzü (UI-01)

Sistemin kullanıcı arayüzü, web tabanlı bir dashboard üzerinden sunulacaktır. Arayüz tasarımında sadelik, tutarlılık ve kullanıcı dostu deneyim ön planda tutulacaktır. Aşağıda sistemin temel ekranları ve beklenen davranışlar açıklanmaktadır.

Giriş ve Kimlik Doğrulama Ekranı Kullanıcıların e-posta adresi ve şifre ile sisteme giriş yapabileceği ekrandır. Yeni kayıt oluşturma işlevini de içerecektir. Başarısız giriş denemelerinde kullanıcıya anlaşılır hata mesajları gösterilecektir.

Ana Kontrol Paneli (Dashboard) Kullanıcının sisteme giriş yaptiktan sonra karşılaştırı ana ekrandır. Bu ekranda; daha önce yüklenen sözleşmelerin listesi, her sözleşmenin mevcut durumu (inceleniyor, tamamlandı, onay bekliyor gibi), genel risk dağılımı istatistikleri ve hızlı erişim kısayollar yer alacaktır.

Sözleşme Yükleme Ekranı Kullanıcınin yeni bir sözleşme dosyası yükleyebildiği ekrandır. Sürükle-bırak ve dosya seçici yöntemlerini destekleyecektir. Kabul edilen dosya formatları ve maksimum dosya boyutu konusunda kullanıcıya önceden bilgi verilecektir. Dosya format ve boyut doğrulaması istemci tarafında anlık olarak yapılacaktır.

Sözleşme İnceleme ve Analiz Ekranı İncelenen sözleşmenin detaylı görünümüdür. Sol panelde ayrıştırılmış sözleşme maddelerinin listesi; sağ panelde seçili maddenin tam metni, atandığı kategori, risk seviyesi, politika uyumluluk durumu ve varsa revizyon önerisi gösterilecektir. Maddeler risk seviyelerine göre renk kodlaması ile görsel olarak ayrıştırılacaktır (örn. düşük risk için yeşil, kritik risk için kırmızı tonları).

Karşılastırmalı Görünüm (Redline) Ekranı Orijinal madde metni ile önerilen revizyon metninin yan yana veya satır içi karşılastırmalı biçimde gösterildiği ekrandır. Metne eklenen kısımlar ve silinen kısımlar farklı renklerle vurgulanarak kullanıcıin değişiklikleri hızlıca kavraması sağlanacaktır.

Onay Akışı Paneli Her sözleşme maddesi için karar verme ekranidır. Kullanıcı, her madde için onayla, reddet veya yeniden revize et seçeneklerinden birini işaretleyebilecektir. Her karara açıklayıcı yorum eklenebilir. Daha önce verilmiş kararların geçmişi kronolojik olarak listelenecektir. İsteğe bağlı olarak toplu karar verme (birden fazla maddeyi aynı anda onaylama/reddetme) desteği sunulacaktır.

Rapor ve Dısa Aktarım Ekranı İnceleme sürecinin sonuçlarının özet ve detaylı rapor olarak görüntülendigi ekrandır. Raporlar; toplam madde sayısı, risk seviyesi dağılımı, verilen kararların özeti ve madde bazlı detayları içerecektir. Kullanıcı, raporları ve revize edilmiş sözleşme taslağını dosya olarak indirebilecektir.

Playbook Yönetim Ekranı Kullanıcıının kendi sözleşme politikalarını oluşturduğu ve yönettiği ekrandır. Kabul edilebilir madde ifadeleri, reddedilmesi gereken hükümler ve eşik değerler bu ekran üzerinden tanımlanacaktır. Mevcut Playbook kurallari listelenebilecektir, düzenlenebilecektir ve silinebilecektir.

## Genel Kullanıcı Arayüzü Gereksinimleri:

- Arayüz responsive tasarima sahip olacak ve masaüstü tarayıcılarda (minimum $1280 \times 720$ piksel çözünürlük) görüntüleme sağlayacaktır.

- Tüm kullanıcı işlemleri için anlık görsel geri bildirim sağlanacaktır (yükleniyor gösteresi, başarı bildirimi, hata mesajı vb.).

- Sözleşme analizi, risk skorlama sırasında kullanıcıya ilerleme durumu gerçek zamanlı olarak bildirilecektir.

- Arayüz dili Türkçe olacaktır.

## Veri Elemanları:

Kullanıcı arayüzü üzerinden sağlanacak ve görüntülenecek temel veri elemanları aşağıda belirtilmiştir:

- Sözleşme dosyası (girdi): PDF veya DOCX formatinda, maksimum 10 MB boyutunda dosya.

- Madde listesi (çıktı): Madde sıra numarası (tam sayı), madde metni (metin), kategori (metin), risk seviyesi (düşük/orta/yüksek), güven skoru (0-1 arası ondalık).

- Revizyon önerisi (çıktı): Orijinal metin (metin), önerilen metin (metin), fark görünümü (HTML formatında).

- Karar bilgisi (girdi): Karar türü (onaylandı/reddedildi/revize), kullanıcı yorumu (metin, isteğe bağlı).

- Rapor (çıktı): Özet rapor verileri (sayısal istatistikler), detaylı rapor (madde bazlı tablo formatında).

## 2.3.3 LLM Servisi Arayüzü

Sistem, madde sınıflandırma, risk değerlendirme, revizyon önerisi üretimi ve doğal dil anlama görevlerini yerine getirmek için harici bir büyük dil modeli servisine bağlanacaktır. İletişim, standart API çağrılarıyla sağlanacak ve veri alışverişinde JSON formatı kullanılacaktır.

- Arayüz tipi: Gerçek zamanlı veri transferi (istek/yanıt).

- Öncelik: Yüksek - analiz işlemlerinin temel bağımlılığdır.

- Veri formati: JSON (UTF-8 kodlamalı metin).

- Güvenlik: API anahtari ile kimlik doğrulama; HTTPS üzerinden şifrelenmiş iletişim.

## 2.3.4 Veritabanı Arayüzü

Kullanıcı hesaplari, sözleşme meta verileri, ayrıştırılmış madde kayıtları, risk değerlendirme sonuçları, onay kararları ve denetim izi (audit trail) verilerinin kalıcı olarak saklanması için ilişkisel bir veritabanı kullanılacaktır.

## 2.3.5 Vektör Arama Arayüzü

Sözleşme maddelerinin ve Playbook kurallarının vektörel temsillerinin saklanması ve anlamsal benzerlik araması yapılması için bir vektör arama bileşeni kullanılacaktır.

## 2.3.6 Önbellek Arayüzü

Kullanıcı oturum bilgilerinin, ajan iş akışı durumlarının ve sık erişilen verilerin geçici olarak saklanması için bir bellek ici (in-memory) veri deposu kullanılacaktır. Bu bileşen, tekrarlayan sorguların hızlandırılması ve kisa ömürlü durum verilerinin yönetilmesi amacıyla görev yapacaktır.

## 2.3.7 Nesne Depolama Arayüzü

Kullanıcıların yüklediği sözleşme dosyalarının (PDF, DOCX) ve sistem tarafından üretilen rapor dosyalarının güvenli biçimde saklanması için bir nesne depolama (object storage) servisi kullanılacaktır.

## 2.3.8 İletişim Yöntemleri

Sistem bileşenleri arasındaki iletişimde aşağıdaki protokoller kullanılacaktır:

<table border="1"><tr><td>Protokol</td><td>Katman</td><td>Kullanım Amacı</td></tr><tr><td>HTTPS/REST/JSON</td><td>Uygulama</td><td>Sunucu tarafı API uç noktalar ile istemi ve harici servisler arasındaki yapılanırılmış veri alışverisi.</td></tr><tr><td>WebSocket(WSS)</td><td>Uygulama</td><td>Uzun süren ajan işlemleri(sözleşme analizi,risk skorlama,revizyon üretimi)sırasında kullanıcıya gerçek zamanlı ilerleme bildirimi gönderilmesi.</td></tr><tr><td>TCP/IP</td><td>İletim</td><td>Veritabanı,önbellek ve nesne depolama bileşenlerine yapılan iç ağ bağlantılar.</td></tr></table>

## 2.4 YKE Dahili Arayüz Gereksinimleri

Sistemin dahili arayüzleri, çok ajanlı yapı içindeki bileşenler arasındaki iç iletişimi kapsar.

Aşağıdaki dahili arayüzler tanımlanmıştır:

1. Orkestratör – Ajan İletişimi: Orkestrasyon mekanizması, ayrıştırma ajanı, sınıflandırma ajanı, risk değerlendirme ajanı ve müzakere ajanı arasındaki görev dağıtım ve sonuç toplama iletişimi yapılandırılmış mesaj formatıyla (JSON) gerçekleştirilecektir.

2. API Katmani - Ajan Katmani: Sunucu tarafi API, ajan orkestratörüne görev başlatma istekleri gönderecek ve sonucları alacaktır. Bu iletişim, asenkron kuyruk veya doğrudan fonksiyon çağrısı mekanizmasıyla sağlanacaktır.

3. Ajan Katmanı – Veri Katmanı: Ajanlar, veritabanı ve vektör arama altyapısına erişim için ortak bir veri erişim katmanı (repository pattern) kullanacaktır.

4. Konteyner İçi İletişim: Konteynerize edilen servisler arasındaki iletişim, iç ağ (internal network) üzerinden sağlanacaktır.

## 2.5 YKE Dahili Veri Gereksinimleri

Sistem, farklı veri türlerinin etkin yönetimi için çok katmanlı bir veri depolama stratejisi kullanacaktır.

## 2.5.1 İlişkisel Veritabanı

Yapılandırılmış verilerin kalıcı olarak saklanması için ilişkisel bir veritabanı yönetim sistemi kullanılacaktır. Aşağıdaki temel veri kümeleri sistemde yer alacaktır:

1. Kullanicilar: Kullanıcı hesap bilgileri: benzersiz tanımlayıcı (id), e-posta adresi, şifre hash değeri, ad-soyad, hesap oluşturma tarihi, son güncelleme tarihi ve aktiflik durumu.

2. Sözleşmeler: Yüklenen sözleşmelerin meta verileri: benzersiz tanımlayıcı, ilişkili kullanıcı referansı, dosya adı, depolama yolu, yükleme tarihi, işleme durumu (yüklendi, işleniyor, tamamlandı, hata) ve toplam madde sayısı.

3. Maddeler: Ayrıştırılmış sözleşme maddeleri: benzersiz tanımlayıcı, ilişkili sözleşme referansı, madde sıra numarası, orijinal metin, atanan kategori, güven skoru.

4. Risk Değerlendirmeleri: Risk analizi sonuçları: benzersiz tanımlayıcı, ilişkili madde referansı, risk seviyesi (düşük/orta/yüksek), risk gerekçesi açıklaması, değerlendirme tarihi.

5. Revizyon Önerileri: Üretilen alternatif ifade önerileri: benzersiz tanımlayıcı, ilişkili madde referansı, önerilen metin, kullanılan bağlam bilgisi, oluşturma tarihi.

6. Onay Kararlar: Madde bazlı karar kayıtlar: benzersiz tanımlayıcı, ilişkili madde referansı, karar türü (onaylandı/reddedildi/revize), kullanıcı yorumu, karar veren kullanıcı referansı, karar tarihi ve zaman damgası.

7. Politika Tanımları (Playbook): Kullanıcı politika kayıtları: benzersiz tanımlayıcı, ilişkili kullanıcı referansı, politika adı, açıklama, kural kümesi (yapılandırılmış veri formatında), oluşturma ve güncelleme tarihleri.

8. Denetim Günlüğü (Audit Log): Sistemdeki tüm kritik işlemlerin denetim kaydı: benzersiz tanımlayıcı, ilişkili kullanıcı referansı, işlem tipi, detay açıklaması ve zaman damgası.

## 2.5.2 Vektör Veritabanı

1. Sözleşme maddelerinin ve Playbook kurallarının anlamsal temsilleri (embedding vektörleri), vektörel arama yapilabilecek bir altyapında saklanacaktır.

2. Vektör boyutu, kullanılan embedding modeline uygun olarak yapilandırılabilir olacaktır.

3. Anlamsal benzerlik sorguları için uygun bir mesafe metriği (cosine similarity vb.) ile indeksleme yapılacaktır.

4. Vektör veritabanı, ilişkisel veritabanı ile entegre çalışabilecek; madde ve politika kayıtları arasında referans bütünlüğü korunacaktır.

## 2.5.3 Önbellek ve Durum Yönetimi

1. Kullanıcı oturum bilgileri, bellek içi veri deposunda saklanacaktır. Oturum süresi yapılandırılabilir olacaktır.

2. Ajan iş akışı durumları (orkestrasyon durum bilgileri), geçici olarak bellek içi depoda tutulacaktır.

3. Sık erişilen Playbook kuralları ve referans madde verileri önbellege alınarak tekrar-layan sorguların hızlandırılması sağlanacaktır.

4. Önbellek verileri için uygun bir geçersizleştirme (cache invalidation) stratejisi uygulanacaktır.

## 2.5.4 Dosya Depolama

1. Yüklenen sözleşme dosyaları (PDF, DOCX) nesne depolama servisinde kullanıcı bazlı mantüksal klasör yapısında saklanacaktır.

2. Dosyalara doğrudan yetkisiz erişim engellenecektir.

## 2.6 Uyarlama Gereksinimleri

1. Sistem, farklı hukuki alanlara (kira sözleşmeleri, ticari anlaşmalar, iş sözleşmeleri vb.) uyarlanabilecek şekilde yapılandırılabilir olacaktır. Bu uyarlama, Playbook kurallari ve sınıflandırma kategorileri aracılığıyla gerçekleştirilecektir.

2. İlk sürümde yalnızca Türkçe dil desteği sunulacak olup, dil parametresi yapılandırilabilir bir şekilde tasarlanacak ve gelecekte çoklu dil desteği eklenebilecektir.

3. Risk değerlendirme rubriği ve eşik değerler, farklı sektörel ihtiyaçlara göre ayarlanabilecektir.

4. Dosya boyutu üst limiti, desteklenen dosya formatları ve zaman aşımı süreleri gibi işletimsel parametreler ortam değişkenleri veya yapilandırma dosyaları aracılığıyla değiştirilebilecektir.

## 2.7 Emniyet Gereksinimleri

1. Sistem, hukuki tavsiye niteligi taşımaz ve bir avukatın yerini almayı hedeflemez. Nihai karar ve sorumluluk her zaman kullanıcıya aittir. Bu uyarı, analiz sonuç ekranlarında açıkça gösterilecektir.

2. Yüksek risk seviyesindeki maddelerde otomatik onay mekanizması uygulanmayacak; bu maddelerde insan onayı zorunlu olacaktır. Bu önlem, hatalı otomatik onaydan kaynaklanabilecek ticari ve hukuki zararları önlemeye yöneliktir.

3. Yapay zeka modelinin ürettiği tüm çıktılar (sıniflandırma, risk skoru, revizyon önerisi), deterministik olmayan doğası gereği yanlış pozitif veya yanlış negatif sonuçlar içerebilir; bu nedenle çapraz doğrulama mekanizmaları uygulanacak ve kullanıcıya sonuçların "yapay zeka destekli ön değerlendirme" niteliğinde olduğu bildirilecektir.

4. Kritik işlemlerde (toplu onay, sözleşme silme vb.) kullanıcıdan onay istenerek kazara yapılan işlemler önlenecektir.

## 2.8 Güvenlik ve Gizlilik Gereksinimleri

1. Kullanıcı şifreleri, endüstri standardı tek yönlü hash algoritmaları (bcrypt veya argon2) ile saklanacaktır.

2. Şifreler en az 12 karakter uzunluğunda olacaktır.

3. Token geçerlilik süresi maksimum 60 dakika olacaktır.

4. 3 başarısız girişten sonra hesap 5 dakika kilitlenecktir.

5. Kimlik doğrulama token'lar imzalanacak ve geçerlilik süresi sınırlandırılacaktır.

6. Harici servis anahtarlari ve kimlik bilgileri, ortam değişkenlerinde veya güvenli bir sır yönetimi (secret management) çözümünde saklanacak; kaynak kodda açık metin olarak bulunmayacaktır.

7. Kullanıcılar yalnızca kendi hesaplarma ait sözleşmelere ve verilere erişebilecektir (yetkilendirme kontrolü).

8. Tüm güvenlik olayları (başarısız giriş denemeleri, yetki ihlali girişimleri vb.) loglanacaktır.

9. İstemci ile sunucu arasındaki tüm iletişim HTTPS protokolü üzerinden şifrelenecek tir.

10. Kullanıcıların yükledigi sözleşme verileri üçuncü taraflarla paylaşılmayacaktır. Harici LLM servisine gönderilen veriler için gizlilik politikası kullanıcıya açıkça bildirilecektir.

11. Kullanıcı istediğinde hesabına ait tüm verilerin silinmesini talep edebilecektir.

## 2.9 YKE Ortam Gereksinimleri

1. Sistem, konteyner teknolojisi (Docker) destekleyen herhangi bir Linux tabanlı sunucu ortamında çalıştırılabilecektir.

2. İstemci tarafı için modern web tarayıcıları (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari'nin güncel sürümleri) desteklenecktir.

3. Tüm sunucu tarafı bileşenlerinin birbirinden izole, tekrarlanabilir ve ortam bağımsız biçimde çalıştırılabilmesi için bir konteynerizasyon platformu kullanılacaktır.

## 2.10 Bilgisayar Kaynak Gereksinimleri

## 2.10.1 Bilgisayar Donanim Gereksinimleri

Sunucu tarafi için asgari donanım gereksinimleri:

- İşlemci: En az 4 çekirdekli x86_64 mimarisi işlemci.

- Bellek (RAM): Minimum 8 GB RAM (16 GB önerilir).

- Disk Alanı: Minimum 50 GB SSD depolama (veritabanı, dosya depolama ve konteyner imajları dahil).

- Ag: Minimum 100 Mbps ag bağlantısı.

Istemci tarafi için:

- Güncel web tarayıcıı çalıştırabilen herhangi bir masaüstü veya dizüstü bilgisayar.

- Minimum $ 1 2 8 0 \times7 2 0 $ piksel ekran çözünürlüğü.

## 2.10.2 Bilgisayar Donanımı Kaynak Kullanımı Gereksinimleri

1. Normal işletim koşullarında (5 eş zamanlı kullanıcı) sunucu CPU kullanımı ortalama %60'in altında kalacaktır.

2. Bellek kullanımı, tahsis edilen RAM kapasitesinin %80'ini aşmayacaktır.

3. Disk I/O performansı, veritabanı sorgularının ortalama 50 ms altında yanıt vermesini sağlayacak düzeyde olacaktır.

## 2.10.3 Bilgisayar Yazılım Gereksinimleri

Sistemin çalışması için gereken yazılım bileşenleri:

- İşletim Sistemi: Linux (Ubuntu 22.04 LTS veya eşdegeri).

- Konteyner Platformu: Docker ve Docker Compose.

- Veritabanı: İlişkisel veritabanı yönetim sistemi (PostgreSQL veya eşdegeri).

- Önbellek: Bellek içi veri deposu (Redis veya eşdegeri).

- Nesne Depolama: S3 uyumlu nesne depolama servisi (MinIO veya eşdegeri).

- Vektör Veritabanı: Vektörel arama altyapısı (Qdrant, Pinecone veya eşdegeri).

## 2.10.4 Bilgisayar İletişim Gereksinimleri

1. Sunucu, harici LLM API servisine kesintisiz HTTPS erişimi sağlayacaktır.

2. Konteynerler arası iletişim, Docker iç ağı (bridge network) üzerinden sağlanacaktır.

3. Kullanıcıdan sunucuya iletişim için HTTPS (443 portu) kullanılacaktır.

4. WebSocket bağlantıları için WSS (güvenli WebSocket) protokolü desteklenecektir.

## 2.11 Yazılım Kalite Faktörleri

1. Fonksiyonellik: Sistem, belirtilen tüm işlevsel gereksinimleri eksiksiz olarak yerine getirecektir.

2. Güvenilirlik: Harici dil modeli servisi kesintiye uğradığında, sistem kullanıcıya durumu bildiren uygun bir hata mesajı gösterecek ve daha önce tamamlanmış analiz sonuçlarına erişimi sürdürecektir. Sözleşme madde sınıflandırmasında en az %70 doğruluk oranı hedefflenecektir.

3. İdame Edilebilirlik: Sistem, modüler bir mimari üzerine inşa edilecektir; her bileşen (ajan, API, arayüz vb.) bağimsiz olarak guncellenebilecek ve dağıtılabilecektir. Birim test kapsama oranı en az %60 olacaktır.

4. Erişilebilirlik: Sistem, 7 gün 24 saat erişilebilir olacaktır (planlı bakım süreleri hariç). Konteynerize mimari sayesinde servisler, hata durumunda hızlı bir şekilde yeniden başlatılabilecektir.

5. Esneklik: Playbook mekanizması aracılığıyla farklı sektörlere ve hukuki alanlara uyarlanabilecektir. Yeni sınıflandırma kategorileri ve risk rubrik parametreleri yapılandırma ile eklenebilecektir.

6. Taşınabilirlik: Sistem, konteyner teknolojisi aracılığıyla farklı işletim sistemlerinde (Linux, macOS, Windows) çalıştırılabilecektir. Tüm konfigürasyon parametreleri, ortam değişkenleri veya harici yapılandırma dosyaları ile yönetilecek; kod içine sabit kodlanmayacaktır.

7. Yeniden Kullanılabilirlik: Ajan mimarisi, farklı doküman analiz senaryolarında yeniden kullanılabilecek şekilde tasarlanacaktır.

8. Test Edilebilirlik: Birim, entegrasyon ve uçtan uca test senaryoları CI/CD hattında otomatik olarak çalıştırılacaktır.

9. Kullanılabilirlik: Yeni kullanıcı onboarding sürecini maksimum 5 dakika içinde tamamlayabilmelidir, hukuki terminolojiye aşina olmayan kullanıcılar için açıklayıcı etiketler ve ipuçları sunulacaktır. Kullanıcı sözleşme yükleme işlemini en fazla 3 adımda gerçekleştirebilmelidir.

## 2.12 Tasarım ve Uygulama Kısıtlamaları

1. Sistem, doğal dil işleme ve metin üretimi görevlerinde harici bir büyük dil modeli (LLM) servisine bağımlidır. Bu servisin erişilebilirliği ve yanıt kalitesi, sistem performansını doğrudan etkileyecektir.

2. Optik karakter tanıma (OCR) doğruluğu, yüklenen taranmış dokümanların görüntü kalitesine bağlidır; düşük çözünurlüklü veya bozuk taramalar hatalı metin çıktısına yol açabilecektir.

3. İlk sürümde yalnızca Türkçe sözleşme metinleri desteklenecktir.

4. Yapay zeka modelinin ürettiği tüm çıktılar, deterministik olmayan doğası gereği yanlış pozitif veya yanlış negatif sonuclar içerebilecektir.

5. Kod tabanı, dilin ve çerçevenin belirlediği stil kılavuzlarma ve en iyi uygulamalara uygun olacaktır.

6. Sürekli entegrasyon ve sürekli dağıtım (CI/CD) hattı aracılığıyla otomatik derleme, test ve dağıtım süreçleri uygulanacaktır.

7. Kod tabanı, versiyon kontrol sistemi (Git) üzerinde yönetilecektir.

8. Veritabanı seması, migration araçları ile versiyonlanacak ve şema değişiklikleri geri alınabilir olacaktır.

9. Büyümenin beklendigi alanlar (çoklu dil desteği, gelişmiş analiz modülleri) için genişleyebilir bir mimari sağlanacaktır.

## 2.13 Personelle Ilgili Gereksinimler

1. Sistem, eş zamanlı en az 5 aktif kullanıcıyı kabul edilebilir performans düzeyinde destekleyecektir.

2. Bireysel kullanıcılar, KOBİ yöneticileri ve hukuk danışmanları olmak üzere farklı yetenek seviyelerindeki kullanıcı grupları desteklenecektir. Hukuki ön bilgi gerektirmeyen, sezgisel bir arayüz sunulacaktır.

3. Hata mesajlar açık ve anlaşılır olacak; kullanıcıyi sonraki adıma yönlendirecektir.

4. Kritik göstergeler (risk renk kodlaması, onay durumları) görsel olarak belirgin biçimde sunulacaktır.

## 2.14 Eğitimle İlgili Gereksinimler

1. Sistem, ilk kullanımayönelik bir başlangıçrehberi (onboarding wizard) içerecektir.

2. Playbook oluşturma ve sözleşme analizi süreçleri için bağlam içi yardım metinleri (tooltip, info box) sağlanacaktır.

3. Kullanıcı dokümantasyonu (kullanım kılavuzu) web tabanlı olarak erişilebilir olacaktır.

4. Sistem yöneticileri için kurulum, yapılandırma ve bakım süreçlerini kapsayan teknik dokümantasyon hazirlanacaktır.

## 2.15 Lojistikle Ilgili Gereksinimler

1. Sistem, Docker imajları olarak paketlenecek ve konteyner kayıt defterinde (container registry) yayımlanacaktır.

2. Dağıtım ve kurulum için Docker Compose veya eşdegeri orkestrasyon dosyaları sağlanacaktır.

3. Sistem güncellemeleri, sifir kesinti veya minimum kesinti ile uygulanabilecek şekilde tasarlanacaktır.

4. Yedekleme ve geri yükleme prosedürleri dokümante edilecektir.

## 2.16 Diger Gereksinimler

1. API yanıt süreleri (harici LLM çağrıları hariç) ortalama 500 milisaniyen altında olacaktır.

2. Sözleşme analizi, toplu risk değerlendirme gibi uzun süren işlemlerde zaman aşımı mekanizması uygulanacak ve kullanıcıya bildirilecektir.

3. Sistem, beklenmeyen bir hata sonrasında veri buttünlüğünü koruyacak şekilde kurtarılabilir olacaktır.

## 2.17 Ambalajlama Gereksinimleri

1. Sistem, Docker konteyner imajları olarak paketlenecektir. Her mikro servis/bileşen ayrı bir imaj olarak dağıtılacaktır.

2. İmajlar, sürüm etiketi (tag) ile versiyonlanacak ve konteyner kayıt defterinde saklanacaktır.

3. Dağıtım paketi; Docker Compose dosyası, ortam değişkenleri örnek dosyası (.env.example) ve kurulum talimatlarını (README) içerecektir.

## 2.18 Gereksinimlerin Önceligi ve Kritikliği

<div align="center">

Aşağıdaki tablo, gereksinimlerin göreceli önem sırasını belirtmektedir:

</div>

<table border="1"><tr><td>Gereksinim Alanı</td><td>Öncelik</td><td>Kritiklik</td><td>Açıklama</td></tr><tr><td>Güvenlik ve Gizlilik</td><td>Çok Yüksek</td><td>Kritik</td><td>Kullanıcı verileri ve sözleşme içeriklerinin korunması.</td></tr><tr><td>Emniyet (İnsan Onayı)</td><td>Çok Yüksek</td><td>Kritik</td><td>Yüksek riskli maddelerde otomatik onay engeli.</td></tr><tr><td>Fonksiyonel Gereksinimler (Analiz)</td><td>Yüksek</td><td>Yüksek</td><td>Ayrıştırma, sınıflandırma, risk analizi temel işlevleri.</td></tr><tr><td>Dış Arayüz (Kullanıcı Ara-yüzü)</td><td>Yüksek</td><td>Yüksek</td><td>Kullanıcı deneyiminin sağlanması.</td></tr><tr><td>Dahili Veri Gereksinimleri</td><td>Yüksek</td><td>Yüksek</td><td>Veri bütünlüğü ve kalıcılık.</td></tr><tr><td>Performans</td><td>Orta</td><td>Orta</td><td>Yanıt süreleri ve eş zamanlı kullanıcı desteği.</td></tr><tr><td>Uyarlama ve Esneklik</td><td>Orta</td><td>Orta</td><td>Farklı sektörlere uyarlanabilirlik.</td></tr><tr><td>Eğitim ve Dokümantasyon</td><td>Düşük</td><td>Düşük</td><td>Kullanıcı ve yönetici kılavuzları.</td></tr><tr><td>Lojistik</td><td>Düşük</td><td>Düşük</td><td>Dağıtım süreçleri.</td></tr></table>

## 3 EK MATERYALLER

## 3.1 Kullanım Senaryoları Özeti

Aşağıdaki tablo, sistemin destekleyeceği temel kullanım senaryolarını özetlemektedir. Her senaryonun detaylı akışı, alternatif akışları ve hata durumları SDD dokümanında ele alınacaktır.

## 3.1.1 Genel Kullanım Senaryosu Diyagrami

Şekil 1, sistemin tüm kullanım senaryolarını ve aktörlerle olan ilişkilerini genel bir bakışla göstermektedir.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734565.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=TQ773%2BzK9l48AHg5XMjt%2BLS2nDE%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 1: Genel Kullanım Senaryosu (Use Case) Diyagrami

</div>

## 3.1.2 Kullanım Senaryoları Tablosu

<table border="1"><tr><td>ID</td><td>Senaryo</td><td>Açıklama</td></tr><tr><td>UC-01</td><td>Kullanıcı Kaydı ve Girişi</td><td>Kullanıcı sisteme kayıt olur ve kimlik doğrula ması ile giriş yapar.</td></tr><tr><td>UC-02</td><td>Sözleşme Yükleme</td><td>Kullanıcı, incelenmesini istediği sözleşme dosya-sını sisteme yükler.</td></tr></table>

<table border="1"><tr><td>ID</td><td>Senaryo</td><td>Açıklama</td></tr><tr><td>UC-03</td><td>Otomatik Ayrıştırma ve Sınıflandırma</td><td>Sistem, yüklenen sözleşmeyi maddelere ayırır ve her maddeyi hukuki kategorilere sınıflandırır.</td></tr><tr><td>UC-04</td><td>Risk Analizi Görüntüleme</td><td>Kullanıcı, her maddenin risk seviyesini, risk gerekçesini ve politika uyumluluk durumunu inceler.</td></tr><tr><td>UC-05</td><td>Revizyon Önerisi İnceleme</td><td>Kullanıcı, riskli maddeler için üretilen alternatif ifadeleri görüntüler, karşılasştırır ve değerlendirir.</td></tr><tr><td>UC-06</td><td>Madde Bazlı Karar Verme</td><td>Kullanıcı, her madde için onay, red veya yeniden revize kararı verir ve gerekirse yorum ekler.</td></tr><tr><td>UC-07</td><td>Karşılasştırmalı İnceleme (Redline)</td><td>Kullanıcı, orijinal ve önerilen metinleri yan yana karşılasştırmalı görünümde inceler.</td></tr><tr><td>UC-08</td><td>Rapor Oluşturma ve İndirme</td><td>Kullanıcı, inceleme sonuçlarını özet veya detaylı rapor olarak görüntüler ve dosya formatında indirir.</td></tr><tr><td>UC-09</td><td>Playbook Oluşturma ve Yönetimi</td><td>Kullanıcı, kendi sözleşme politikalarını tanımlar, düzenler ve analiz için etkinleştirir.</td></tr><tr><td>UC-10</td><td>Revize Sözleşme Dısa Aktarımı</td><td>Kullanıcı, onaylanan değişikliklerle güncellenmiş sözleşme taslağını dosya olarak indirir.</td></tr><tr><td>UC-11</td><td>Kullanıcı ve Sistem Yapılandırması Yönetimi</td><td>Sistem yöneticisi, kullanıcı hesaplarını ve sistem yapılandırma parametrelerini yönetir.</td></tr></table>

## 3.1.3 Kullanım Senaryosu Diyagramları

Aşağıda her bir kullanım senaryosunun detaylı diyagramları yer almaktadır.

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734620.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=5IXEpcD0uk7mQ95zR8%2FfXGMLri4%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 2: UC-01: Kullanıcı Kaydı ve Girişi

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734642.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=DUNGLNfF6lDTkb3w9CCYHtHij8I%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 3: UC-02: Sözleşme Yükleme

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734652.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=o5IVfIKJE2TaGet%2F7PioO0A28Os%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 4: UC-03: Otomatik Ayrıştırma ve Sınıflandırma

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734664.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=D0HnZ08OQkLqUDtfcXd1orE0s8s%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 5: UC-04: Risk Analizi Görüntüleme

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734672.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=pXyVH7frp3H3qbCw18YEVMSJWbM%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 6: UC-05: Revizyon Önerisi Inceleme

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734680.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=FfDpAsI2OVSOLXYjOGkVKB3s%2BmU%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 7: UC-06: Madde Bazli Karar Verme

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734690.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=RR05aQrZwkOVOHhP9G9VFt59NlA%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 8: UC-07: Karşılaştırmalı Inceleme (Redline)

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734699.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=pHZfcmDwqKNzjewV6%2FUMMRkgt7o%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 9: UC-08: Rapor Oluşturma ve Indirme

</div>

<div align="center">

UC-09: Playbook Oluşturma ve Yönetimi

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734710.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=QMOITuY5n0mQoBGfU0I6xmG8p2c%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 10: UC-09: Playbook Oluşturma ve Yönetimi

</div>

<div align="center">

UC-10: Revize Sözleşme Dısa Aktarımı

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734723.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=97U3Mk1QatI45%2FqLWq2O3pDQ3NM%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 11: UC-10: Revize Sözleşme Dısa Aktarımı

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734731.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=H%2FvVpxoATY9hLxUIZ5Bzu%2F39smk%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 12: UC-11: Kullanıcı ve Sistem Yapılandırması Yönetimi

</div>

<div style='text-align: center;'><img src='https://maas-watermark-prod-new.cn-wlcb.ufileos.com/ocr%2Fcrop%2F202604191904505d6c16b7a9714091%2Fcrop_1_1776596734741.png?UCloudPublicKey=TOKEN_6df395df-5d8c-4f69-90f8-a4fe46088958&Signature=LmPuti9llhhWSSRBkjQb8iZ36YM%3D&Expires=1777201534' alt='OCR图片'/></div>

<div align="center">

Şekil 13: Genel UML Sınıf Diyagramı

</div>

## 3.2 Veri Akışı Genel Görünümü

## 3.2.1 UML Sınıf Diyagrami

Şekil 13, sistemin nesne yönelimli analiz kapsamındaki genel UML sınıf diyagramını gösterektedir.

## 3.2.2 Veri Akışı

Sistemdeki temel veri akışı aşağıdaki sırayı takip etmektedir:

1. Kullanıcı, sözleşme dosyasını web arayüzü üzerinden yükler.

2. Doküman işleme katmanı, yüklenen dosyayı düz metne dönüştürür (gerektiğinde OCR uygular).

3. Ayrıştırma ajanı, metni bağımsız sözleşme maddelerine böler ve her maddeyi hukuki kategorilere sınıflandırir.

4. Risk değerlendirme ajanı, sınıflandırılmış maddeleri kullanıcı Playbook'u ve referans madde havuzu ile karşılaştırarak risk analizi yapar.

5. Riskli bulunan maddeler için müzakere ajanı, bağlam bilgisini kullanarak alternatif ifade önerileri üretir.

6. Tüm analiz sonuçları (sıniflandırma, risk skoru, revizyon önerisi) kullanıcıya kontrol paneli üzerinden sunulur.

7. Kullanıcı, her madde için onay, red veya yeniden revize kararını verir.

8. Kararlar ve ilişkili yorum bilgileri denetim izi olarak veritabanına kaydedilir.

9. Kullanıcı isteğine bağlı olarak özet/detaylı rapor veya revize edilmiş sözleşme taslağı oluşturularak dışa aktarılır.

## 3.3 Sözlük

<table border="1"><tr><td>Terim</td><td>Tanım</td></tr><tr><td>YKE (Yazılım Konfigülerasyon Elemanı)</td><td>Yazılım sisteminin bağışsız olarak tanımlanabilen, yönetilebilen ve kontrol edilebilen bir bileşeni. Bu projede sistem tamamını ifade eder.</td></tr><tr><td>SRS</td><td>Yazılım Gereksinimleri Belirtimi (Software Requirements Specification). Sistemin işlevsel ve işlevsel olmayan gereksinimlerini tanımlayan doküman.</td></tr><tr><td>SDD</td><td>Yazılım Tasarım Dokümanı (Software Design Document). Sistemin nasıl tasarlanacağı ve uygulanacağı tanımlayan doküman.</td></tr></table>

<table border="1"><tr><td>Terim</td><td>Tanım</td></tr><tr><td>LLM</td><td>Büyük Dil Modeli(Large Language Model).Doğal dil işleme görevlerinde kullanılan yapay zeka modeli.</td></tr><tr><td>RAG</td><td>Retrieval-Augmented Generation.Bilgi erişimi ile metin üretimini birleştiren yapay zeka tekniği.</td></tr><tr><td>OCR</td><td>Optik Karakter Tanıma(Optical Character Recognition).Görüntülerdeki metni dijital metne dönüştürme teknolojisi.</td></tr><tr><td>Playbook</td><td>Kullanıcıının sözleşme inceleme sürecinde kullanılmak üzere tanımladığı politikalar, kurallar ve eşik değerler kümesi.</td></tr><tr><td>Ajan(Agent)</td><td>Belirli bir görev alanında(ayrıştırma,sınıflandırma,risk analizi,müzakere)bağımsız çalışan yapay zeka bileşeni.</td></tr><tr><td>Orkestratör</td><td>Birden fazla ajanın koordineli çalışmasını sağlayan,görev dağıtımı ve sonuç toplama işlemlerini yöneten mekanizma.</td></tr><tr><td>Redline</td><td>Orijinal metin ile önerilen revizyon metni arasındaki farkları görsel olarak gösteren karşılastırmalı görünüm.</td></tr><tr><td>Embedding</td><td>Metin verilerinin, anlamsal benzerlik araması yapılabilecek sayısal vektör temsillerine dönüştürülmesi.</td></tr><tr><td>CI/CD</td><td>Sürekli Entegrasyon/Sürekli Dağıtım(Continuous Integration/Continuous Deployment).Otomatik derleme,test ve dağıtım süreçleri.</td></tr><tr><td>Audit Trail</td><td>Denetim İzi.Sistemde gerçekleştirilen tüm kritik işlemlerin kaydını tutan günlük mekanizması.</td></tr><tr><td>API</td><td>Uygulama Programlama Arayüz(Application Programming Interface).Yazılım bileşenleri arasındaki iletişimi sağlayan arayüz.</td></tr><tr><td>REST</td><td>Temsili Durum Transferi(Representational State Transfer).Web servisleri için kullanılan mimari yaklaşım.</td></tr><tr><td>WebSocket</td><td>İstemci ile sunucu arasinda çift yönlü,gerçek zamanlı iletişim sağlayan protokol.</td></tr><tr><td>KOBİ</td><td>Küçük ve Orta Büyüklükteki İşletme.</td></tr></table>