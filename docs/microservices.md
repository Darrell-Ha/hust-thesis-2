<<Lời nói giới thiệu gì đó....>>

# Kiến trúc Monolithic

Kiến trúc Monolithic hay còn gọi là cấu trúc một khối là mẫu thiết kế được áp dụng rộng rãi trong các ứng dụng và hệ thống hiện nay. Các thành phần của chương trình được phát triển phụ thuộc lẫn nhau và trong một nền tảng được thống nhất ngay từ ban đầu cho đến tới khi hoàn thiện để sử dụng.

Nhờ tính đơn giản, dễ dàng xây dựng và triển khai nên kiến trúc một khối đã được phố biển rộng rãi và được áp dụng trong nhiều các ứng dụng phần mềm như các phần mềm hỗ trợ quá trình kinh doanh cho doanh nghiệp ERPs, CRMs,....

![monolithic-architecture](images\mono-archi.png)

(mô hình kiến trúc Monolithic, nguồn: [Viblo.asia](https://images.viblo.asia/647a9906-db1f-44a8-afe9-e699b464d849.png))

Ứng dụng được xây dựng theo kiến trúc Monolithic sẽ có những thuận lợi như:

- Có thể hỗ trợ cho các client cả trên browser, desktop và mobile. Điều này nhờ vào việc ứng dụng đã gói gọn tính năng và database trong một khối nguyên. Để ứng dụng hoạt động, hỗ trợ client trên các nền tảng khác nhau thì ta chỉ cần xây dựng giao diện người dùng tương ứng cho từng nền tảng mà người dùng sử dụng.

- Ứng dụng khi sử dụng có thể cung cấp một số APIs cho bên thứ ba và đồng thời tích hợp với các ứng dụng khác thông qua các cơ chế giao tiếp như REST, SOAP,...

- Quá trình phát triển nhanh chóng vì đã có sự thống nhất về công nghệ và kiểm thử dự án dễ dàng. Đồng thời quá trình triển khai cũng không phức tạp vì toàn bộ dự án đã được gói gọn trong một khối.

Tuy nhiên, do các thành phần của ứng dụng bị phụ thuộc vào nhau quá nhiều nên khi thay đổi một thành phần cũng sẽ gây ảnh hưởng đến các thành phần còn lại. Điều đó cũng gây cản trở khi phát triển và tái cấu trúc lại một thành phần nào đó trong dự án. Thay đổi một thành tố đồng nghĩa với việc phải cập nhật lại toàn bộ hệ thống sẽ gây nên nhiều phiền toái, chưa kể đến là các vấn đề mới nảy sinh trong quá trình cập nhật. Vì vậy, khi dự án trở nên lớn mạnh và phức tạp, kiến trúc monolithic sẽ tự trở thành một rào cản lớn khi mà ứng dụng cần mở rộng và cập nhật để đáp ứng yêu cầu từ người dùng, cho thấy Monolithic là một kiến trúc có tính ổn định, tính mở rộng chưa cao. Kiến trúc Monolithic đạt hiệu quả cao với những dự án có quy mô vừa và nhỏ hoặc các ứng dụng không có quá nhiều chức năng. Để phù hợp và giải quyết những mong muốn dễ dàng mở rộng và bảo trì, phù hợp với các hệ thống lớn, kiến trúc Microservice được nói tới đây sẽ là một giải pháp tốt mà các hệ thống, nền tảng lớn đang áp dụng như Netflix, Spotify,...

# Kiến trúc Microservices

## Thế nào là kiến trúc microservices

Kiến trúc Microservices là kiến trúc hướng đến mục tiêu chia nhỏ hệ thống trở thành các dịch vụ - services nhỏ độc lập. Mỗi dịch vụ được xây dựng khép kín bởi một đội ngũ phát triển nhỏ và có một mã nguồn riêng, cơ sở dữ riêng và chỉ được dùng để triển khai một nghiệp vụ nào đó.

Nhờ vậy, các services có thể dễ đàng được nâng cấp và bảo trì mà không cần phải xây dựng lại hoặc là triển khai lại toàn bộ hệ thống ứng dụng.

![micro-architecture](images\micro-archi.png)
(nguồn: [microsoft learn - microservices](https://learn.microsoft.com/en-us/azure/architecture/includes/images/microservices-logical.png))

Microservices có thể được coi là một biến thể của kiến trúc hướng dịch vụ (_service-oriented architecture_). Các nguyên tắc để xây dựng nên một hệ thống SOA như là

- các dịch vụ cũng cần được phát triển và triển khai một cách độc lập cùng với tính kết nối lỏng lẻo giữa các services - _loose coupling_.

- Các services thường giao tiếp với nhau thông qua các API, đồng thời các services cũng cung cấp các API cho các hệ thống bên ngoài truy cập vào một số phần nhất định để tương tác.

Microservices cũng đều có các nguyên tắc ở trên nhưng có một số điểm khác biệt có thể kể đến đó là ở phạm vị áp dụng kiến trúc. Trong SOA, các services được chia sẻ với nhau về tài nguyên và được tái sử dụng nhằm mục tiêu liên kết giữa các ứng dụng của doanh nghiệp, tổ chức. Còn với Microservices, các ứng dụng được cô lập cả về xây dựng, triển khai và tài nguyên nhằm mục tiêu giao tiếp giữa các thành phần trong một ứng dụng.

![img soa-vs-microservices](images\soa-vs-micro.png)
(nguồn internet, cre: [xenonstack](https://cloudgeeks.net/wp-content/uploads/2020/11/image-4.png))

Ngoài ra, trong kiến trúc microservices có thể có thêm một số thành phần như:

- Management/orchestration: giúp cân bằng các services trên các nodes hoặc instance và xác định lỗi trong quá trình chạy.

- API Gateway: Trạm cho phép chuyển các yêu cầu từ client đến các microservices tương ứng. Việc sử dụng API Gateway là một tùy chọn của hệ thống và nó đem lại nhiều lợi ích dễ dàng nâng cấp và tái cấu trúc mà không cập nhật bên phía clients. Đồng thời giúp tách biệt các quá trình xác thực, ghi log, giải mã bảo mật và cân bằng tải. Ngoài ra còn có thể thực hiện phân quyền để áp dụng chính sách theo yêu cầu của hệ thống.

## Lợi ích và hạn chế của Microservices

Phát triển hệ thống một cách nhanh chóng là một lợi thế khi ứng dụng microservice vào triển khai xây dựng hệ thống. Bởi vì các microservices được triển khai độc lập với nhau nên rất dể dàng quản lý, tránh lỗi toàn bộ hệ thống và dễ dàng kiểm thử, sửa lỗi một cách nhanh chóng và tái cấu trúc gọn gàng.

Hơn nữa, khi phát triển một hệ thống được áp dụng kiến trúc microservices sẽ giúp làm tinh giản mã nguồn. Nhờ việc cô lập các services - tức là không chia sẻ mã nguồn, dữ liệu, kiến trúc microservice giúp giảm đi sự phụ thuộc giúp cho quá trình viết nên những chức năng mới trở nên dễ dàng hơn.

Khả năng mở rộng là một ưu điểm mạnh mẽ mà kiến trúc microservice được cho là vượt trội nhất hiện tại khi mà thay vì khi nâng cấp một service một cách độc lập giúp mở rộng các hệ thống con mà không cần nâng cấp toàn bộ hệ thống phức tạp và cồng kềnh.

Bên cạnh những điểm tích cực mà kiến trúc Microservices đem lại, song khi áp dụng triển khai, ta sẽ cần cân nhắc một số những hạn chế như sau:

1. Sự phức tạp của hệ thống sẽ tăng song hành với số lượng các dịch vụ. Đồng nghĩa với việc quản lý và bảo trì hệ thống trở nên khó khăn hơn. Việc tạo nên các microservices không phải lúc nào cũng giống nhau về công nghệ phát triển, mỗi một service có độ phức tạp khác nhau nên việc tái cấu trúc lại một hệ thống với nhiều microservices cũng như là quản trị nó là một vấn đề khó khăn. Đây là một thách thức khi ta mong muốn phát triển ứng dụng một cách nhanh chóng.

2. Xuất hiện đỗ trễ cao hơn. Việc sử dụng nhiều dịch vụ cũng nghĩa là hệ thống đã có nhiều bước giao tiếp hơn. Ngoài ra, nếu như một hoạt động cần nhiều service tham gia liên tiếp nhau sẽ tạo thêm độ trễ trong việc kết nối và đợi phản hồi. Từ đó, thiết kế các microservices cần phải tính toán kĩ càng khi viết các API. Một số các nhà chuyên gia nhận định đây là một vấn đề thường gặp và tất yếu khi áp dụng mô hình và giải pháp đề xuất đó cần áp dụng những định dạng tuần tự hóa - serialization hay sử dụng những mấu giao tiếp không đồng bộ như bộ cân bằng tải dựa trên hàng đợi.

3. Chưa đủ đảm bảo Tính toàn vẹn dữ liệu (_Data Integrity_) khi mỗi service chịu trách nhiệm cho dữ liệu của bản thân nó. Càng có nhiều service, mức độ khó khăn cũng tăng theo và trở thành một thách thức lớn.

4. Cần một đội ngũ vận hành có kinh nghiệm và chuyên môn cao với những hệ thống microservices lớn.

## Một số Pattern trong thiết kế

### API Gateway Pattern

Khi hệ thống đã được chia thành các microservices, số lượng các microservices có thể lên tới vài trăm. Việc tương tác với dịch vụ khi đó trở nên lộn xộn và phức tạp, thậm chí có thể kéo theo những vấn đề liên quan khác cả về mặt kĩ thuật lẫn logic của hệ thống, dẫn dần gây nên tình trạng mất kiểm soát các services.

Chẳng hạn khi độc giả truy cập vào trang báo điện tử nào đó ngoài những thông tin hiển thị về các tin tức mới được cập nhật gần đây còn có thêm một số những tin tức hot được phân loại theo danh mục như thời sự, kinh doanh, thể thao, ngoài ra còn một số công cụ như thông báo, đăng nhập và cả những thông số về giá vàng, tỉ số các trận đấu ở các giải vô địch quốc gia, bình luận trên các bài viết,... Như vậy, độc giả sẽ cần phải thực hiện gọi các request đến các service thông báo, đề xuất tin tức theo danh mục và các service khác để trang báo hiển thị được đầy đủ thông tin. Hay nói cách khác, cần bao nhiêu mục thông tin thì cần gọi thủ tục một lượng như vậy. Trên đây là một ví dụ trên một ứng dụng web đơn giản khi áp dụng microservices. Trong các ứng dụng phức tạp hơn, các công việc kể trên thậm chí còn phải làm nhiều hơn nữa. Ngoài ra, trong các hệ thống microservice, các dịch vụ này có thể sử dụng những giao thức không thân thiện với web như là RPC, AMPQ,... các giao thức phù hợp với giao tiếp nội bộ, dẫn đến khó khăn cho người sử dụng khi mà ứng dụng cho phép người dùng truy cập trực tiếp services nhưng chưa có phương thức giao tiếp phù hợp.

Cũng vì những yếu tố trên, ta rất ít khi cho phép người dùng có thể truy cập trực tiếp vào các services mà sử dụng một bên trung gian. Đó chính là tiền đề giúp cho cách sử dụng API Gateway trở nên phổ biến trong các hệ thống sử dụng các mô hình Microservices.

![api-gateway](images\api-gateway.png)

API Gateway đóng vai trò là cửa ngõ giúp giao tiếp giữa người dùng với hệ thống. API Gateway cung cấp riêng API cho từng client cụ thể. Thông thường, ta thường hay tích hợp luôn nhiệm vụ liên quan đến bảo mật như xác thực, giám sát và các nhiệm vụ khác hỗ trợ cho quá trình giao tiếp giữa người dùng và hệ thống trở nên trơn tru như cân bằng tải, bộ nhớ đệm, định tuyến các request đến các service sao cho phù hợp với nhu cầu của người dùng.

API Gateway cũng có một số hạn chế. Việc lượng lớn truy cập vào API Gateway trong trường hợp tệ nhất có thể trở thành một nút thắt cổ chai của hệ thống - tắc nghẽn và khi mà API Gateway bị lỗi đẫn đến cả hệ thống bị lỗi. API Gatway là một máy chủ cần phải có tính sẵn sàng cao nên ta cần phải đảm bảo các yêu cầu kĩ thuật phần cứng và phần mềm, phù hợp với hoạt động và quá trình bảo trì. Mặc dù có các hạn chế kể trên, song cách tiếp cận bằng việc sử dụng API Gateway trong các hệ thống áp dụng microservices vẫn luôn là một lựa chọn tốt và nên được sử dụng.

### Service Discovery Pattern

Như ở phần trên đã nhắc tới, số lượng dịch vụ trong một hệ thống áp dụng Microservices là khá lớn. Trong quá trình vận hành, các dịch vụ sẽ thực hiện tương tác với nhau để thu được kết quả nào đó nên việc giao tiếp giữa các dịch vụ diễn ra liên tục và thường xuyên, chưa kể đến những sự tương tác giữa các microservices với lượng người dùng đông đảo. Việc gọi đến một thực thể dịch vụ có sẵn thông qua được thực hiện thông qua việc hệ thống hiểu và biết các thông tin về vị trí mạng của thực thể cần gọi tới, cụ thể ở đây là địa chỉ IP và port. Tuy nhiên, các hệ thống áp dụng microservices hiện được xây dựng và triển khai trên nên tảng điện toán đám mây, cùng với đó là các vị trí này cũng dễ dàng thay đổi linh hoạt nên việc thực hiện truy tìm dịch vụ là một việc khá khó khăn. Vì vậy, bài toán được đưa ra là đó là ta cần có một cơ chế để có thể thực hiện tìm kiếm và gọi dịch vụ một cách nhanh chóng và chính xác.

Trong cách tiếp cận này, có hai mô hình hay được sử dụng chủ yếu đó là client-side discovery và server-side discovery.

Với mô hình client-side discovery, client sẽ cần phải tự mình xác định vị trí của các services khả dụng thông qua việc truy vấn một cơ sở dữ liệu đặc biết đó là Service Registry và áp dụng thuật toán cân bằng tải để chọn ra dịch vụ cần tìm.

![service-discovery-cli-side](images\service-discovery-cli-side.png)

Mô hình này được áp dụng để giải quyết vấn đề về sự linh hoạt trong vị trị của các thực thể dịch vụ. Quá trình hoạt động có thể mô tả như sau:

- Khi khởi động dịch vụ, ghi vị trí mạng vào trong service registry và xóa bỏ khi thực thể dịch vụ này kết thúc

- Cập nhật những thông tin của các thực thể dịch vụ theo chu kỳ để cập nhật vào Service Registry

Tuy nhiên, sự hiệu quả của mô hình trên lại phụ thuộc khá nhiều vào sự ràng buộc giữa client và service registry.

Đến với mô hình server-side discovery, sự khác nhau giữa mô hình này với mô hình client-side discovery năm ở chỗ Client sẽ thực hiện request đến một dịch vụ nào đó thông qua một bộ cân bằng tải (load balancer). Bộ cân bằng tải sẽ truy vấn đến thay Client thực hiện truy vấn đến Service Registry.

![service-discovery-server-side](images\service-discovery-server-side.png)

Server-side discovery cũng có những lợi thế như:

- Quá trình tìm kiếm tách biệt với client nên mã lệnh sẽ được đơn giản hơn, tránh được sự phụ thuộc giữa client và service registry.

- Việc áp dụng mô hình trên trở nên đễ dàng hơn khi mà đã có một sô những môi trường triển khai sẵn mô hình này (như Kubernetes, AWS Elastic Load Balancer,...).

Tuy nhiên, nếu như không áp dụng các môi trường triển khai đã được tích hợp sẵn cân bằng tải thì ta sẽ cần phải tự cài đặt và quản lý sẽ phức tạp đôi chút.

### Lever-link

### saga 

### comunication

---

### Event-Driven Pattern

### Command Query Responsibility Segregation (CQRS) pattern
