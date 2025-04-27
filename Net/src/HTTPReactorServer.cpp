#include "HTTPReactorServer.h"
#include "Poco/AutoPtr.h"
#include "Poco/NObserver.h"
#include "Poco/Net/HTTPServerRequest.h"
#include "Poco/Net/HTTPServerRequestImpl.h"
#include "Poco/Net/HTTPServerResponse.h"
#include "Poco/Net/HTTPServerResponseImpl.h"
#include "Poco/Net/HTTPServerSession.h"
#include "Poco/Net/SocketNotification.h"
#include "Poco/Net/SocketReactor.h"
#include "Poco/Net/SocketAcceptor.h"
#include "Poco/Net/ServerSocket.h"
namespace Poco {
	namespace Net {
	

class HTTPReactorServerConnection;

class HTTPReactorServer 
{
public:
	HTTPReactorServer(int port, int maxConnections);
	~HTTPReactorServer();

	void start();
	void stop();
private:
	Poco::Net::SocketReactor _reactor;
	Poco::Net::ServerSocket _serverSocket;
	Poco::Net::SocketAcceptor<HTTPReactorServerConnection> _acceptor;
};

class HTTPReactorServerConnection 
{
public:
	HTTPReactorServerConnection(Poco::Net::SocketReactor& reactor, Poco::Net::StreamSocket socket) {
		_reactor = reactor;
		_socket = socket;
		_reactor.addEventHandler(_socket, Poco::NObserver<HTTPReactorServerConnection, Poco::Net::ReadableNotification>(*this, &HTTPReactorServerConnection::onRead));
		_reactor.addEventHandler(_socket, Poco::NObserver<HTTPReactorServerConnection, Poco::Net::WritableNotification>(*this, &HTTPReactorServerConnection::onWrite));
	}
	~HTTPReactorServerConnection();

	void onRead(const AutoPtr<ReadableNotification>& pNf) {
		try {
			// Handle read event
			AutoPtr<HTTPServerParams> parameters;
			HTTPServerSession session(_socket, parameters);
			// Create request and response objects
			Poco::Net::HTTPServerResponseImpl response(session);
			Poco::Net::HTTPServerRequestImpl request(response, session, nullptr);
			// Process request and generate response
		}
		catch (const Poco::Exception& ex) {
			onError();
		}
	}
	void onWrite(const AutoPtr<WritableNotification>& pNf);
	void onError(const AutoPtr<ErrorNotification>& pNf);
	void onShutdown(const AutoPtr<ShutdownNotification>& pNf);

private:
	Poco::Net::SocketReactor& _reactor;
	Poco::Net::StreamSocket _socket;
	Poco::Net::HTTPServerRequest _request;
	Poco::Net::HTTPServerResponse _response;
	Poco::Net::HTTPServerSession _session;
};
}
};