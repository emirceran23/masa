## YAZILIM TASARIM DOKÜMANI

## İÇİNDEKİLER

1 KAPSAM ... 2

1.1 Tanım 2

1.2 Sisteme Genel Bakış ... 2

1.3 Dokümana Genel Bakış ... 2

2 İLGİLİ DOKÜMANLAR ... 2

3 YKE ÇAPINDA TASARIM KARARLARI ... 2

4 YKE’NIN YAPISAL TASARIMI ... 2

4.1 YKE Bileşenleri ... 2

4.2 Genel Çalıştırma (execution) Kavramı ... 3

4.3 Arayüz Tasarımı ... 3

5 YKE DETAYLI PLANI ... 3

6 GEREKSINIMLERIN IZLENEBILIRLIĞI ... 4

7 NOTLAR ... 4

8 EKLER ... 4

## 1.1 Tanim

Bu paragraf, tanımlama numarası(ları), başlık(ları), kısaltma(ları), versiyon numarası(ları) ve yayın numarası(ları) dahil bu dokümanın uygulandığı sistemin tam olarak tanımlamasını içerir.

## 1.2 Sisteme Genel Bakış

Bu paragraf, bu dokümanın uygulandığı sistem ve yazılımın amacını kısaca ifade eder. Sistemin ve yazılımın genel yapısını tanımlar; sistem geliştirme, operasyon ve bakımın geçmişini özetler; müşteri, kullanıcı, geliştirici ve destek birimlerini tanımlar; şu anki ve planlı işlevsel birlikleri tanımlar ve diğer ilişkili dokümanları listeler.

## 1.3 Dokümana Genel Bakış

Bu paragraf, bu dokümanın amaç ve içeriğini özetler ve ayrıca kullanımla ilişkili tüm güvenlik ve özel hususları tanımlar.

## 2 İLGİLİ DOKÜMANLAR

Bu bölümde, bu dokümanda referans edilen buttün dokümanlar numara, başlık, yayın numarası, değişiklik numarası ve tarihleri olarak listelenir. Ayrıca, buttün dokümanların kaynağı tanımlanır.

## 3 YKE ÇAPINDA TASARIM KARARLARI

Bu bölüm, YKE çapında tasarım kararlarını, yani YKE’nin kullanıcıın bakış açısından nasıl davranacağının tasarımı ile ilgili kararlar ve YKE’yi oluşturan yazılım birimlerinin seçim ve tasarımını etkileyen diğer kararları, sunmak için gerekli paragraflara bölünür.

Tasarım anlamak için gerekli olan tasarım hususları sunulmalı ve bu hususlara atif yapılmalıdır. YKE çapında tasarım kararları örnekleri aşağıdadır:

a. YKE'nin kabul edeceği girdiler ve üreteceği çıktılar ile ilgili tasarım kararları.

b. Her girdi veya koşula göre YKE davranış ile ilgili tasarım kararları.

c. Veri tabanları/veri dosyalarının kullanıcıya nasıl görüneceği ile ilgili tasarım kararlari.

d. Emniyet, güvenlik ve gizlilik gereksinimlerini karşılamak için seçilen yaklaşım.

e. İstenilen esnekliği, elde edilebilirliği, idame ettirilebilirliği sağlamak üzere seçilen yaklaşım gibi gereksinimlere cevap olarak alınan diğer YKE çapında tasarım kararları.

## 4 YKE'NIN YAPISAL TASARIMI

Bu bölüm YKE'nin yapısal tasarımını sağlamak üzere aşağidaki paragraflara ayrılır.

## 4.1 YKE Bileşenleri

Bu paragraf;

a. Yazılım Konfigürasyon Elemanını oluşturulan yazılım birimlerini tanımlar. Her bir yazılım birimine projeye özel tanımlayıcı atanmalıdır.

NOT: Bir yazılım birimi bir Yazılım Konfigürasyon Elemanının tasarımındaki mantüksal bir elemandır; örneğin bir Yazılım Konfigürasyon Elemanının ana alt bölümü, bu alt bölümün bir bileşeni, bir sınif, nesne, modül, fonksiyon, rutin veya veri tabanı. Yazılım birimlerinin statik ('oluşur' gibi) ilişki(leri)'ni gösterir. Seçilen yazılım tasarım metodolojisine (örneğin bir nesneye yönelik tasarımda bu paragraf sınif ve nesne yapıları dışında YKEnin modül ve süreç yapısını da sunabilir) bağmlı olarak çoklu ilişkiler sunulabilir.

b. Her bir yazılım biriminin amacını belirtir ve YKE gereksinimleri ve ona tahsis edilen YKE çapında tasarım kararlarını tanımlar.

c. Her bir yazılım biriminin geliştirme durum/türünü tanımlar (yeni tasarım, mevcut tasarım veya yazılımın olduğu gibi tekrar kullanılması, mevcut tasarım veya yazılımın tekrar mühendisliğe tabi tutulması, tekrar kullanım için yazılım geliştirilmesi, yapı N için yazılım planlaması) Mevcut tasarım veya yazılım için, açıklama; isim, versiyon, dokümantasyon referansları, kütüphane gibi tanımlayıcı bilgileri sağlar.

d. YKE’nin (uygulanabildiği kadar her bir yazılım biriminin), bilgisayar donanım kaynaklarının (işlemci kapasitesi, bellek kapasitesi, girdi/çıktı alet kapasitesi, yardımcı bellek kapasitesi ve haberlesme/iletişim ağı techizat kapasitesi) planlanmış kullanımını açıklar.

## 4.2 Genel Çalıştırma (execution) Kavrami

Bu paragraf, yazılım birimleri arasında çalışma kavramını tanımlar. Yazılım birimlerinin dinamik ilişkilerini (yani uygulanabildigi kadar çalışma kontrolünün akışı, veri akışı, dinamik olarak kontrol edilen ardışıklık, durum geçiş diyagramları, zamanlama diyagramları, birimler arası öncelikler, yarida kesintilerle başa çıkılması, zamanlama/ardışıklık ilişkileri, istisnaların idaresi, aynı zamanlı çalıştırma (execution) dinamik olarak tahsis etme/boşaltma, nesnelerin, süreçlerin, görevlerin dinamik olarak oluşturulması/silinmesi ve dinamik davranışın diğer yönlerini içeren YKE işlemi sırasında nasıl etkileşceklerini) gösteren diyagramlar ve tanımlamaları içermelidir.

## 4.3 Arayüz Tasarımı

Bu paragraf, her bir arayüz atanan projeye özel tanımlayıcısinı belirtir ve arayüz elemanlarını (yazılım birimleri, sistemler, konfigürasyon elemanları, kullanıcılar vs.) isim, numara, versiyon ve dokümantasyon referanslarına göre uygulanabildiği kadar tanımlar. Tanımlama, hangi elemanların önceden belirlenmiş arayüz özelliklerine sahip olduğunu ve hangilerinin geliştirildiğini veya değiştirildiğini belirtmelidir.

## 5 YKE DETAYLI PLANI

Bu paragraf projeye özel tanımlayıcı ile bir yazılım birimini tanımlar ve birimi belirtir. Tanımlama uygulanabildiği kadar aşağıdaki bilgileri içerir.

a. Birim tasarım kararları eğer varsa, daha önce seçilmemiş kullanılacak algoritmalar gibi birim tasarım kararları

b. Yazılım biriminin tasarımındaki her türlü kısıtlamalar, sınırlandırmalar, veya alışılmamış özellikler

c. Kullanılacak programlama dili ve belirlenenden farklı bir dil kullanılmışa kullanım mantığı ile ilgili açıklamalar

d. Eğer yazılım birimi işlevsel komutlardan (form ve raporları tanımlamak için bir Veri Tabanı Yönetim Sistemindeki menü seçimleri, veri tabanı erişimi ve kullanımı için çevrim-içi (on-line) Veri Tabanı Yönetim Sistemi sorguları, otomatik kod oluşturmak için Grafiksel Kullanıcı Arayüzü (Graphical User Interface)hazirlayanlara (input) girdi, işletim sistemi veya dış senaryo (shell script) komutları gibi) oluşuyorsa veya onları içeriyorsa, işlevsel komutların bir listesi verilir ve kullanıcı kılavuzları veya onları açıklayan diğer dokümanlara atif yapılır.

e. Eğer yazılım birimi veri içeriyor, aliyor ve çıkartıyorsa, mümkün olduğu kadar, girdilerin, çıktıların ve diğer veri elemanlarının ve veri eleman gruplarının açıklaması.

f. Eğer yazılım birimi mantık içeriyorsa, yazılım birimi tarafından kullanılacak mantık uygulanabiligi kadar aşağıdakileri içerir,

1) Icrasının başlaması esnasında yazılım birimi içindeki etkin durumlar

2) Kontrolün diğer yazılım birimlerine geçtiği durumlar

3) Veri çevrimi konversiyonu, tekrar isimlendirme ve veri transfer işlemlerini içeren her bir girdiye cevap ve yanıt süresi

4) Yazılım birimi işlemi sırasında, işlemler zinciri ve dinamik olarak kontrol edilen sıralamalar aşağıdakileri içerir:

a) Sıralama kontrolü için yöntem

b) Bu yöntemin mantık ve girdi durumları (Zamanlama sapmaları, öncelik atamaları gibi)

c) Bellek içi ve dışı veri transferi

d) Ayrı bir giriş sinyalinin hissedilmesi ve yazılım birimi içindeki akışı kesen işlemler arasındaki zamanlama ilişkileri.

e) Istisna ve hata giderme

## 6 GEREKSINIMLERIN IZLENEBILIRLIGI

Bu bölüm şunları içerir:

a. Yazılım Tasarım Dokümanında (YTD) belirtilen her bir yazılım biriminden ona tahsis edilen YKE gereksinimlerine kadar olan izlenebilirlik.

b. Yazılım Konfigürasyon Elemanı gereksinimlerinden onun tahsis edildiği yazılım birimlerine kadar izlenebilirlik.

## NOTLAR

Bu bölüm bu dokümanın anlaşılmasına yardımcı olan her turlü genel bilgiyi içerir. (örneğin geçmiş bilgi, sozlük, açıklama) Bu bölüm tüm kısaltmaların ve onların bu dokümanda kullanılan anlamların listesini ve bu dokümanı anlamak için gerekli olan terim ve tanımların listesini içermelidir.

## 8 EKLER

Ekler, dokümanın anlaşılmasını kolaylaştırmak için ayrı ayrı basılmış olarak kullanılabilir (örneğin grafikler, tasnif edilmiş veri). Ekler kullanımda kolaylığı sağlamak için ayrı dokümanlar olarak ciltlenebilirler. Ekler, alfabetik olmalıdır (A, B, vs).