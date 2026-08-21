/**
 * SAFEISOL Tracker
 * Единый JS-модуль для сбора событий: клики, просмотры, скролл, время, поиск и т.д.
 */

(function () {
    'use strict';

    // ─── Утилиты ──────────────────────────────────────────────

    function getCookie(name) {
        var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }

    function setCookie(name, value, days) {
        var expires = '';
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + days * 86400000);
            expires = '; expires=' + date.toUTCString();
        }
        document.cookie = name + '=' + value + expires + '; path=/; SameSite=Lax';
    }

    function generateId() {
        return 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'.replace(/x/g, function () {
            return ((Math.random() * 16) | 0).toString(16);
        });
    }

    function getVisitorId() {
        var id = getCookie('visitor_id');
        if (!id) {
            id = generateId();
            setCookie('visitor_id', id, 365);
        }
        return id;
    }

    function getSessionId() {
        var id = getCookie('session_id');
        if (!id) {
            id = generateId();
            setCookie('session_id', id, 0); // session cookie
        }
        return id;
    }

    function getParam(name) {
        var params = new URLSearchParams(window.location.search);
        return params.get(name) || '';
    }

    function getCsrfToken() {
        var match = document.cookie.match(new RegExp('(^| )csrftoken=([^;]+)'));
        return match ? match[2] : '';
    }

    // ─── Отправка события ─────────────────────────────────────

    function trackEvent(eventType, data) {
        var payload = Object.assign(
            {
                event_type: eventType,
                url: window.location.href,
                product: getProduct(),
                category: getCategory(),
                metadata: {}
            },
            data || {}
        );

        // Браузерные данные кладём в metadata
        payload.metadata.screen = window.screen.width + 'x' + window.screen.height;
        payload.metadata.viewport = window.innerWidth + 'x' + window.innerHeight;
        payload.metadata.device_type = detectDeviceType();
        payload.metadata.language = navigator.language || '';
        payload.metadata.timezone = '';
        try {
            payload.metadata.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
        } catch (e) {}

        // UTM и referrer
        var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
        utmKeys.forEach(function (key) {
            var val = getParam(key);
            if (val) payload.metadata[key] = val;
        });
        if (document.referrer) {
            payload.metadata.referrer = document.referrer;
        }

        // Connection
        if (navigator.connection) {
            payload.metadata.connection = navigator.connection.effectiveType || '';
        }

        // Язык интерфейса ОС
        if (navigator.platform) {
            payload.metadata.platform = navigator.platform;
        }

        // Отправляем
        try {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/track/', true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            var csrfToken = getCsrfToken();
            if (csrfToken) {
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
            }
            xhr.send(JSON.stringify(payload));
        } catch (e) {
            // Тихо — трекер не должен ломать сайт
        }
    }

    function getProduct() {
        var el = document.querySelector('.section-title');
        return el ? el.textContent.trim() : '';
    }

    function getCategory() {
        var el = document.querySelector('.breadcrumbs a:nth-child(2)');
        if (el) return el.textContent.trim();
        // fallback: попробуем из URL
        var match = window.location.pathname.match(/\/category\/([^/]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function detectDeviceType() {
        var w = window.innerWidth || document.documentElement.clientWidth;
        if (w <= 576) return 'mobile';
        if (w <= 1024) return 'tablet';
        return 'desktop';
    }

    // ─── Инициализация visitor_id и session_id ────────────────

    getVisitorId();
    getSessionId();

    // ─── 1. Просмотр страницы (page_view) ────────────────────

    trackEvent('page_view');

    // ─── 2. Просмотр товара (product_view) ────────────────────

    if (getProduct()) {
        trackEvent('product_view');
    }

    // ─── 3. Просмотр каталога ─────────────────────────────────

    if (window.location.pathname === '/catalog/') {
        trackEvent('catalog_view');
    }

    // ─── 4. Просмотр категории ─────────────────────────────────

    if (window.location.pathname.indexOf('/category/') === 0) {
        trackEvent('category_view');
    }

    // ─── 5. Клик по телефону ──────────────────────────────────

    document.addEventListener('click', function (e) {
        var link = e.target.closest('a[href^="tel:"]');
        if (link) {
            trackEvent('phone_click', {
                metadata: { phone: link.getAttribute('href').replace('tel:', '') }
            });
        }
    });

    // ─── 6. Клик по хлебным крошкам ───────────────────────────

    document.addEventListener('click', function (e) {
        var crumb = e.target.closest('.breadcrumbs a');
        if (crumb) {
            trackEvent('breadcrumb_click', {
                metadata: {
                    crumb_text: crumb.textContent.trim(),
                    crumb_href: crumb.getAttribute('href')
                }
            });
        }
    });

    // ─── 7. Отправка заявки (форма) ──────────────────────────

    var contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function () {
            trackEvent('lead_submit', {
                metadata: {
                    form_id: 'contactForm'
                }
            });
        });
    }

    // ─── 8. Скачивание документов ─────────────────────────────

    document.addEventListener('click', function (e) {
        var doc = e.target.closest('.document');
        if (doc) {
            var nameEl = doc.querySelector('.name');
            trackEvent('doc_download', {
                metadata: {
                    doc_name: nameEl ? nameEl.textContent.trim() : ''
                }
            });
        }
    });

    // ─── 9. Опросный лист (отдельная ссылка) ─────────────────

    document.addEventListener('click', function (e) {
        var link = e.target.closest('.questionnaire');
        if (link) {
            trackEvent('doc_download', {
                metadata: {
                    doc_name: 'Опросный лист',
                    doc_href: link.getAttribute('href')
                }
            });
        }
    });

    // ─── 10. Переключение вкладок товара ─────────────────────

    document.addEventListener('click', function (e) {
        var tab = e.target.closest('.product-navbar-li a');
        if (tab) {
            var parent = tab.parentElement;
            if (parent && parent.id) {
                trackEvent('product_tab', {
                    metadata: {
                        tab: parent.id.replace('navbar-', '')
                    }
                });
            }
        }
    });

    // ─── 11. Просмотр изображения товара ─────────────────────

    document.addEventListener('click', function (e) {
        // Клик по миниатюре
        var miniImg = e.target.closest('.mini-img');
        if (miniImg) {
            var img = miniImg.querySelector('img');
            trackEvent('product_image_view', {
                metadata: {
                    image: img ? img.getAttribute('src') : ''
                }
            });
        }

        // Клик по основному изображению (открытие модалки)
        var mainImg = e.target.closest('#main-image');
        if (mainImg) {
            trackEvent('product_image_view', {
                metadata: {
                    image: mainImg.getAttribute('src'),
                    action: 'open_modal'
                }
            });
        }
    });

    // ─── 12. Навигация по сайту (клики по ссылкам шапки) ──────

    document.addEventListener('click', function (e) {
        var navLink = e.target.closest('.navbar-a, .navbar-a-selected, .lnav__link');
        if (navLink) {
            trackEvent('page_view', {
                metadata: {
                    navigation_click: true,
                    nav_text: navLink.textContent.trim(),
                    nav_href: navLink.getAttribute('href')
                }
            });
        }
    });

    // ─── 13. Поиск по сайту ──────────────────────────────────

    // Отслеживаем ввод в поле поиска (с дебаунсом)
    var searchInput = document.getElementById('searchInput');
    var searchDebounce = null;
    if (searchInput) {
        searchInput.addEventListener('input', function () {
            var query = this.value.trim();
            clearTimeout(searchDebounce);
            if (query.length > 1) {
                searchDebounce = setTimeout(function () {
                    trackEvent('search_query', {
                        metadata: {
                            query: query
                        }
                    });
                }, 1000);
            }
        });
    }

    // Мобильный поиск
    var mobSearchInput = document.querySelector('.mob-search .find');
    var mobSearchDebounce = null;
    if (mobSearchInput) {
        mobSearchInput.addEventListener('input', function () {
            var query = this.value.trim();
            clearTimeout(mobSearchDebounce);
            if (query.length > 1) {
                mobSearchDebounce = setTimeout(function () {
                    trackEvent('search_query', {
                        metadata: {
                            query: query,
                            mobile: true
                        }
                    });
                }, 1000);
            }
        });
    }

    // Клик по результату поиска
    document.addEventListener('click', function (e) {
        var searchResult = e.target.closest('#searchResults a');
        if (searchResult) {
            trackEvent('search_click', {
                metadata: {
                    query: searchInput ? searchInput.value.trim() : '',
                    result_text: searchResult.textContent.trim(),
                    result_href: searchResult.getAttribute('href')
                }
            });
        }
    });

    // ─── 14. Глубина скролла ──────────────────────────────────

    var maxScrollPercent = 0;
    var scrollTracked = { 25: false, 50: false, 75: false, 100: false };

    function updateScrollDepth() {
        var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        var docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        if (docHeight <= 0) return;
        var percent = Math.round((scrollTop / docHeight) * 100);

        if (percent > maxScrollPercent) {
            maxScrollPercent = percent;
        }

        [25, 50, 75, 100].forEach(function (threshold) {
            if (maxScrollPercent >= threshold && !scrollTracked[threshold]) {
                scrollTracked[threshold] = true;
                trackEvent('scroll_depth', {
                    metadata: {
                        depth: threshold,
                        page_height: docHeight
                    }
                });
            }
        });
    }

    var scrollDebounce = null;
    window.addEventListener('scroll', function () {
        clearTimeout(scrollDebounce);
        scrollDebounce = setTimeout(updateScrollDepth, 200);
    });

    // ─── 15. Время на странице ────────────────────────────────

    var pageStartTime = Date.now();
    var timeTracked = false;

    // Отправляем время при уходе со страницы
    function sendTimeOnPage() {
        if (timeTracked) return;
        timeTracked = true;
        var seconds = Math.round((Date.now() - pageStartTime) / 1000);
        if (seconds < 2) return; // Не отправляем, если сразу ушли
        trackEvent('time_on_page', {
            metadata: {
                seconds: seconds,
                max_scroll: maxScrollPercent
            }
        });
    }

    // sendBeacon — работает даже при закрытии вкладки
    window.addEventListener('beforeunload', function () {
        if (timeTracked) return;
        timeTracked = true;
        var seconds = Math.round((Date.now() - pageStartTime) / 1000);
        if (seconds < 2) return;
        var payload = JSON.stringify({
            event_type: 'time_on_page',
            url: window.location.href,
            product: getProduct(),
            category: getCategory(),
            metadata: {
                seconds: seconds,
                max_scroll: maxScrollPercent,
                screen: window.screen.width + 'x' + window.screen.height,
                viewport: window.innerWidth + 'x' + window.innerHeight,
                device_type: detectDeviceType(),
                language: navigator.language || '',
                timezone: ''
            }
        });
        navigator.sendBeacon('/api/track/', new Blob([payload], { type: 'application/json' }));
    });

    // Fallback для старых браузеров
    window.addEventListener('pagehide', sendTimeOnPage);

})();