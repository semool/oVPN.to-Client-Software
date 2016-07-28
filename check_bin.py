# -*- coding: utf-8 -*-
#
# CHECK_BIN

import os
import sys
import time
import hashlib
import struct
import subprocess
import threading

BITS = struct.calcsize("P") * 8

MODE="UNSIGNED"

HASHS_DB = { 
		32: {
			"UNSIGNED": {"libxmlxpat.dll": "96e1a67feb5874f0e9fd9dad4933b396363dc6315057919c2777067c2c484006a2be8cbb08536508c79850b2924a77cc87cc71ebc3162cda0cc529f3fb60dffd", "libgirepository-1.0-1.dll": "29f845fedaf7a4ab22d512f5664ebc006b5843e5395460f5d79258a8eb570c2ecca30affa0ef924aa17e706b6e1d890dc93539da32ffbf6dafdf1574c9696e1e", "libffi-6.dll": "cf975d9bc3c48fbe2a3cfb2b7838b63ad5aef3efec4d686e2959d4f5f5544b6725f921de17c675cf244d3f3be097b327a07f15edc258f81023460bd629563e78", "libfreetype-6.dll": "1b7832b59d8c46a90a30d593004c2373158e22d9cff9611bcff7b3ddfd6ec5cb0ab2f602aa6ba820ad1dcb5bf01192cad654c319c7f8ca02816378756e2b1b89", "libgdk-3-0.dll": "98cb4a9d85f8715503ca24eb44bb6600a0b2a93aa488c247bd820a4d3a7427851b97b2cb341ec73fe31e223208ffbc1741ff2a648c6c00b64d46aaad9daf1752", "libgdk_pixbuf-2.0-0.dll": "e75c205a49947f946f9544dd5c31b4843cbc2a0a07e53adb1d66474241a05b082aea51f2961fdf8ccfa28dd7da0af00fb6ad5e4acf4b4998008aff5d38802801", "libpangoft2-1.0-0.dll": "386d0377c6f66638ab7d788c3954b91fe9458c249f3c09c2a1d2212c3382d88212cf918c6af7190233bc8fb4ecb144c535e22d8beb58ba83537921cdda6e8495", "libpangocairo-1.0-0.dll": "b464ce50bc5bf8fe5cfbe414c3768106b6344c17f65aecbe21ea41c75698dab7278d4c62f35c44d2665ff4cee92179e899b190c13332de3eaaf9f7dbf13148cc", "libharfbuzz-0.dll": "dbe2b9d82bb5ca3d175f83bb6fe95490e5d0c7338701383db19f0e3d33597899d4f04c2d86877c55d4b8e92b1ba1db30376ca82e7356881005b413e9da818117", "libwebp-5.dll": "ea717297e4b089b3aa4f8582405af1f15c012c68081a05aa7222f13ea0dba1b766b5c7bfa89d964bb28812b0394f60d633f2f69c4b03da9a9e5abf1a1128905a", "libgmodule-2.0-0.dll": "ec6b6d271afd3e4d5628e59cd7c1e3778b0bf2de7a26367589945ce930410985a3bc19433bc6c8a3728f3f8a7b22fb95ab260ad46a2ade28bcb03e514ff0f53d", "libpng16-16.dll": "9e9f3d41d303cc02caee135ab8d2ffc22de28b16b7dc7f15dd8043747a4dde18f8e194bb247d358f173929750fea63a8ac7866d7d338b66eecf89bfbf646f5e1", "librsvg-2-2.dll": "c262ebe5ab6e7fe18fdfe855255656f5ac3fb97131d10d09e1603a192bd809461e11b9709878081292a356c8d9e131703bd906eb486ffa55eaa9d0d880f52e03", "libharfbuzz-gobject-0.dll": "3f07830bf134e03a216a083061f65e608daa17623841a33456400dfe17e2eb4948c373a99f3bad7871d97d711204c09bf84df8c53322bc909187de4ec3a59aec", "libharfbuzz-icu-0.dll": "f1bc1ee9eaace4b567ddda29824501c5883639111b407fcf26d30fc6248d815d3942113fa6b79dc83d3f4fe91f732a3c75e57c4ffd4ed744c5a560bcf823b9ab", "libwinpthread-1.dll": "90eaf5448558c15154cab958086282b26580aebae56b9f395412d8a080c6306e5e17f14f390fc645feca3f44100b101626bc73f0e18554760eb1aebd024e2cd6", "libpangowin32-1.0-0.dll": "1e4287d9763151fa619120704cf42050af8195a280a29627dc43a8f23853e9468f69e874bf1999c1fd92a19dfc852acd32874e43b858b12117319f1996d7976f", "libgailutil-3-0.dll": "31f1c62a4f5866218ac24346b5c22934de6a572534caa9886a7185bd98c65a6bd3df16afdf14685e106419b5010d510e973429b6a53507e39b2f8ae0c25deea8", "libgio-2.0-0.dll": "b7e79fddd233bc4f4b8dcf042cd097f6e8b6c0f224643e33929b1ec819f374bfbf3b8c609cc64d37a702869b83be6cc28c222eeca04de62aeb062342df70ac90", "libjasper-1.dll": "6d134fe47564b2fd606af3ff0e10198aad7da616cc3c2ce52349cc40cf6fe77bd120a9026a88ad89ec3072ea8af8b44a234497aae5ed31ffbd3c31bcde89a73a", "libpango-1.0-0.dll": "390b996c20e404f96eb6899baaf3bfaa728f3093abb310761d0d669659422f07c741485c9087047df2c8434f3c7e1e8547e358758fd2928aefe9e21a7881e6fc", "libfontconfig-1.dll": "550ce4bf4808383e8f8badd0628cbbf7312c4a8045d843da56801210887d1a702caca1f4573e5cc2e230288c80500effdcef3e5919e2d35463bd3e4640e61621", "libgtk-3-0.dll": "971dda6acc873cb4c0907983b19ad9ea7bc58682489901b301805beac94696346c2a2a1141a421af9a8005efe55d220b1c84f0e2329f35749d152e7407c5f3a1", "libglib-2.0-0.dll": "f828f74f522a4e93a5d289dd825fd0659114c634fea2d4defc5ca3025171f2911f909f3875f93be9bd14ce0b9f8888e9a6c869ea27b1bda9ab52f002a7651090", "libgthread-2.0-0.dll": "9bdd1456460581f9d6bf1bd1b40aaa5ef529c6dc67044c362a8bcee4315d606d340e368b73781f8a2816afcd0ff56a1147e25435f1b0ded8c4e9bc200f2df1b0", "python27.dll": "8409e04f44f565c2b1551591c621e36d8caf0e06de0c364bb3772ebdd52259b5fe774eb1478615e842c7ce5b0adc134d0d4e27c6c6c7592e5c269e259e84236b", "libjpeg-8.dll": "fe477a56d98ac87d502f1783c1f53e1b1696adba971b9862895c8ffb1725a1c8112f758323959a95654c8fe235cbbb1ebcb2fc8d0369892a95fd6df9208bdbd9", "libzzz.dll": "9d005ce71f442073a5c8dacad1119110501f4522ff5b3e5d55534ebc835988f59d97696f5266242ce16cc5ee6daa74c37814a8ff822192b4ea591b63ac38bb13", "libatk-1.0-0.dll": "af9ffb557f1a707f400da138e273f3c8488da21a8e979423d7078502936e4682feecb1bbb3a0779cf8a79f79ecc10c964bea9a057e6313f152643f8bfcb7bfa8", "libcairo-gobject-2.dll": "2c9399d06c3aa1ea4ec3044f740cd3a8af83955836f157e86f887f795783a40d1d55f324d6485a22decbbdd5164a78d98b21671fb9df6c6501ca3fc2d4edf13a", "libepoxy-0.dll": "0566d05e05b0a262b6a2aeafd27c09391b1cbe148f2a6aacbc3b7b5264d47d37fb56b59309fddc8dcfff38eb2727ab2bd5ed95724a40d338f9bb5d7eb8fad2c3", "libgobject-2.0-0.dll": "27367baa16bdccd3dac3567f7775d1c75bf6e2e2de1c78ad9faf3629d36677f8e2e5807757044a48e4069884a95d9c6c3e5503673bd04f77c3acb34c248d0050", "libintl-8.dll": "b6cdf51a3f06251f65b49b01b75d894ddc229770a37336c4b8f85cd157ff9606940247dae1a00f3bec693a8dd1b9577dd417d6a718dd5a22df70147908b31be1", "libtiff-5.dll": "b19723e67c0c4b401cb160482a75be5c08643ad6fb9a3bc96fcba192f585ca26d6fbbca925dc2cd8f4dcc7298f6f45387da253d64fe956e824872054a3ee6508"},
			"SIGNED" : {},
		},
		64: {
			"UNSIGNED": {"libxmlxpat.dll": "fa964b21de8d1500164688d29c8847e12cfc494e07fa0334fbb19b96f2dfbf34a7cacfb522857e68ce7cafb5e64c1d371ee8612bde397b837639cdf3b35ee958", "libgirepository-1.0-1.dll": "343efcdf087fdb2667b5c04846b48aaeee4eb720c4117ccbcbb948c7dca2b5d16293e66b3ab53aea344eccd7f9f87f6bf38910b4826862f865e5f32f1e2b8aec", "libffi-6.dll": "498cfa455e1b617333d39cb66a6df1d5aa3b6bfc1b7a491d5b613bcaea8aa82ace8b88ec151d9a64d810091909eba4d7dd42c7cebddf0059d52cf47fd0806582", "libfreetype-6.dll": "9f3a0ccca90613ca3418734f134626f965c9ec6e1903139bf63fd763beb5c4636bc4f2bcb5a5516e689db5121a72ec8229732be7fc793074b0d5ff8fd9ddcbe3", "libgdk-3-0.dll": "9efdcedc2795edb3ea3c66378a9e48f877a5b4901eba504e413a343ea5e822b3a761f72e40f8318df29c8d5861e958c7f873bd44fc04963259c1e3897593a432", "libgdk_pixbuf-2.0-0.dll": "21ac8611de4c1f63ac51f8ac3b9347554dcd08ff8734b2f139e3770dfd9adffb821ceca4ee47f5dec1fdff4354fe4a5b6205fbdc28722e5b3e274280fbff9808", "libpangoft2-1.0-0.dll": "ac4bae5dff704baff42ebc4d2a97e6340fa02f6b45513b7259449d6ec9fb5fab4ac0aba6059dffdff6b107c7cef2586ebf7f6cda5e8fbbe43339dccaea4ac32e", "libpangocairo-1.0-0.dll": "0484559fe1298fab18b0a0866813e740b2dde2cba93ea23ece538fec0e55ea30e10769702d79b73bfbac59cf69c0dc6c3a35579364ab499b6b94759c7a116568", "libharfbuzz-0.dll": "a7c0dd73563cea29678e49ee9e90a0bc941a16f2524c8fe2a2e81a473d3313a95173da8421abff0a56852a72e9d433ab4ad9019de9a857e0429f78d3fd4d8a30", "libwebp-5.dll": "fbdc5d3e0b86c3393a5471594546726887a2529876a68a3c15b6ea6f92c6f20d7dd3d8c758a24acb32f8aa1d8917a86a0cf0d1101f90525d021e8e04e8d62336", "libgmodule-2.0-0.dll": "d149e519c64824bf0e1272d579b067a84f01dfb280a07b4c012622c7b21ea70d810c64657dfa00bcc734a5240c4740dded88522f7a503b4646e44c28f5ef5ba2", "libpng16-16.dll": "fc68ed399df8762b8faab90fd3a635bf2219d41a787dea7d464b8b2e302ddb564b61c93ad1c315a6b751c450a2c01268bc6cbced8b15196ec5c99c6d032b10c7", "librsvg-2-2.dll": "9676ba093ac221dc592368dd1158d62386e2c4c028a0e8ca4740ca8fafb32faf0de5ac61e609b322426c153996e5cabedd958a3c2b36f545c524cfb7c3f6a4d4", "libharfbuzz-gobject-0.dll": "94090fc70536c9cac7c8d90e830e299e977c1595aded3452faa2a5148d4cd4a81a96f8df478e9b5fa0723ed65b2f75a0c410a19313a032685cb548450b8ac769", "libharfbuzz-icu-0.dll": "7fda94b975b32f092292018e8d2140df903faebf320af071c35e7c8476e350227af7b5b31fed4be3f9591f3ac2283c40ad7a70a9159d347c8b4e95ea1b230bbc", "libwinpthread-1.dll": "ecb8d9ab764221f4e7fd4e32f4313271f8d6814032211a8d6e11eebe5fe9cda0181bee65c307209e62a2532cc7ec0ad5a2f90d649efb96f32a4d2a3d0504b2f4", "libpangowin32-1.0-0.dll": "061af23741df0075ecb6cd114e849c3d9600aa876d5aa2aeace7d01dd4905dc5806f6798df0572253e3de927be41c969565b4cc272e88267ed9a05bce9af44d1", "libgailutil-3-0.dll": "867fbebd796ac733b29bc4d03da34f87468f816bce2df052d6494a9e613a1e997ce8086a5b554b307ea56538657e713e8f296d4b4c05a724a0f3d27238713ac1", "libgio-2.0-0.dll": "9dc4cde18025985cf5e7bea2b1390be0970feb2846e1de2610001965dfb87039be7cca666cccbf1e6879817d32fa34307257f77e1fcff9aa6cd916f0c3cf7d15", "libjasper-1.dll": "e3ed592bf18ab851e2ef4c1b0f4ee52dd6e69c5b0d5e17e42fec887ffaeefc4d718fbed4c89c678fae09190c02b9aea1d76c6e9eb49fa712e5871300bf765424", "libpango-1.0-0.dll": "7d6a8072a65f98790dca9a7869684bca43758f26e712198ed4eac2abd19f3e9f631c0269bd31069012edb2b8f977b1c7fd1843f72aae385a5e3674e5045721e2", "libfontconfig-1.dll": "9063fc36ffa7e00ebd21ad519aee480e489307cc2f1641c3da4f4e51afa803445df117d83425a6087227205eae04001bc361f7a4fb66c0617f628d33c0ac17ac", "libgtk-3-0.dll": "0c39af87a16c255314a9282ed9ee08ad739a40bd12c39a43c1751fa20945b48fa96f2262dbe996de209be36b82efa7c5b534fd16c66af4879383132a9895570f", "libglib-2.0-0.dll": "ab74e1f5465306a98642d009ce47fa88feed374827ebb6ef358fe5457c2f22f2e89b2cfed1a360bf62b72c4a84dfb2c9a86c88116f82da109f2701f91b5e5689", "libgthread-2.0-0.dll": "4a75ccaac12639399b118bd803f5ea784eca83459f8cbd50b5f1b6c0cd2a471eff2a9897c991f16e799ba3da8b2c4690d1ceaf539ec70ed1edb44e5894e46484", "python27.dll": "8e12a4c16b8c63d484347279bd0ee0c553eaf1c865f372e26737d2a8621f4b614fe9bd5f2e91fb295bbd9b062137d4a93394893d9a01f14bfc5924be23880376", "libjpeg-8.dll": "4a175439e1e1e3481b9d41b8c5ade0190d040f1dca8a345ab101998444417de4def55b726c42436dde9630591a78fcd03256d90c6b0842503a217f36d3ae9356", "libzzz.dll": "6e151e585f18c5d97cac33297c180d9ca8affe9cc3d7f25dde72a76ed04b466b874038f6abb87bcbf8f778736f9862505297c7d0a74ef4a0c017ce107d283066", "libatk-1.0-0.dll": "1e8a2e040642bc6ad8e82beeca5f177c9cdf4f13b20bff5ab3f1ad1e6b8b30c761020bfe396930eb49bcd27409bdebcee15c04f1f1780c28a23c0149b7823be8", "libcairo-gobject-2.dll": "6b6e3202bdb9bc1fa55d6c5c0e406d0a35914668b4287a14914f3b91cd01590f8f59bb636d39ce3bd301938ed4c7e20447daaed3029f4f4e3f7972a3e8c117f2", "libepoxy-0.dll": "2d73d42b54014bb7de6fffaca476a8edd09830ac20c81cb31a296e601708438a2b52c86f5fbd02b74e217a1de4f493aba9b24f0500df7dd86e0bdedb04f46fa5", "libgobject-2.0-0.dll": "0e65200fcd9ea0f0c1c94b86c3893f344f5d4ada2bf1759b7cc18a6c9107dbed594abde56fa6af8bd990e14491bc33d0fa5069f9ae0edf5bf33319e62d9aa708", "libintl-8.dll": "220085a8ac201ceeb9becc579d2f2f93c59ae0b63445d57e3e2d5aae8516dd23650e1cc2b2d7dc708845d29f78ca7cd6eea5121ba79193294746b917b1387078", "libtiff-5.dll": "1ffe1b54351e8f9818b8771b3f0a6b35019cd6d52278f1b7f6d2678ac596816cbdf730c07b8d06a4f76ec529126b87a978c7ff7d9559fc20dd4fdb4f7ecba25a"},
			"SIGNED" : {},
		},
	}

class CHECK_BIN:
	def __init__(self):
		if self.self_vars():
			if self.verify_files(self.BIN_DIR):
				print "hash check '%s' bits passed" % (BITS)
		else:
			print "init failed"
			sys.exit()

	def self_vars(self):
		self.HASHS_DB = HASHS_DB[BITS][MODE]
		self.BIN_DIR = os.getcwd()
		print "self.BIN_DIR = '%s'" % (self.BIN_DIR)
		print "def self_vars: return True"
		return True

	def hash_sha512_file(self,file):
		if os.path.isfile(file):
			hasher = hashlib.sha512()
			fp = open(file, 'rb')
			with fp as afile:
				buf = afile.read()
				hasher.update(buf)
			fp.close()
			hash = hasher.hexdigest()
			return hash

	def list_files(self,dir):
		files = []
		content = os.listdir(dir)
		for file in content:
			if file.endswith('.dll'):
				filepath = "%s\\%s" % (dir,file)
				files.append(filepath)
		return files

	def verify_files(self,dir):
		notfound, verified, failed, missing  = 0, 0, 0, 0
		verify_files_indir = self.list_files(dir)
		
		try:
			verify_files_store = self.HASHS_DB
		except:
			verify_files_store = {}
		
		if len(verify_files_indir) > 0:
			self.log("\ndef verify_files: verify_files_indir = '%s'" % (dir))
			
			for file in verify_files_store:
				fileshort = file.split("\\")[-1]
				filepath = "%s\\%s" % (dir,file)
				if not filepath in verify_files_indir:
					notfound +=1
					self.log("def verify_files: file = '%s' FILE NOTFOUND" % (filepath))
			
			for file in verify_files_indir:
				fileshort = file.split("\\")[-1]
				if fileshort in self.HASHS_DB and os.path.isfile(file):
					hash = self.hash_sha512_file(file)
					if self.HASHS_DB[fileshort] == hash:
						verified += 1
						#self.log("def verify_files: hashed file = '%s' hash = '%s' OK" % (file,hash))
					else:
						failed += 1
						self.log("def verify_files: file = '%s' HASH FAILED" % (file))
				else:
					missing += 1
					self.log("def verify_files: file = '%s\\%s' MISSING JSON" % (dir,file))
			print "almost leave"
			self.log("def verify_files: key '%s' dir = '%s' filesindir = '%s' filesjson = '%s' missing = '%s' notfound = '%s' failed = '%s' verified = '%s'" % (MODE, dir, len(verify_files_indir), len(verify_files_store), missing, notfound, failed, verified))
			if missing == 0 and notfound == 0 and failed == 0 and verified == len(verify_files_store) and verified == len(verify_files_indir):
				return True
			else:
				self.log("def verify_files: FAILED! EXIT!")
				sys.exit()
		else:
			self.log("no DLLs found in '%s'" % (dir))

	def log(self,text):
		print text
		logfile = "check_bin.log"
		data = "%s\n" % (text)
		fp = open(logfile, "a")
		fp.write(data)
		fp.close()


def app():
	CHECK_BIN()

if __name__ == "__main__":
	app()
	print "leave app"
